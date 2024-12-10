"""Generative question answering with sources."""

import copy
import logging
from typing import AsyncGenerator, Generator

from openai import AsyncOpenAI, OpenAI
from openai.lib.streaming.chat import ChunkEvent, ContentDeltaEvent, ContentDoneEvent
from openai.types.completion_usage import CompletionUsage
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class GenerativeQAOutput(BaseModel):
    """Base class for the expected LLM output."""

    has_answer: bool  # Here to prevent streaming errors
    answer: str
    paragraphs: list[int]


MESSAGES = [
    {
        "role": "system",  # This one can be overriden through env var
        "content": """Given the following extracted parts of a long document and a question, create a final answer with references to the relevant paragraphs.
    If you don't know the answer, just say that you don't know, don't try to make up an answer, leave the paragraphs as an empty list and set `has_answer` to False.

    QUESTION: Which state/country's law governs the interpretation of the contract?
    =========
    Content: This Agreement is governed by English law and the parties submit to the exclusive jurisdiction of the English courts in  relation to any dispute (contractual or non-contractual) concerning this Agreement save that either party may apply to any court for an  injunction or other relief to protect its Intellectual Property Rights.
    Source: 28
    Content: No Waiver. Failure or delay in exercising any right or remedy under this Agreement shall not constitute a waiver of such (or any other)  right or remedy.\n\n11.7 Severability. The invalidity, illegality or unenforceability of any term (or part of a term) of this Agreement shall not affect the continuation  in force of the remainder of the term (if any) and this Agreement.\n\n11.8 No Agency. Except as expressly stated otherwise, nothing in this Agreement shall create an agency, partnership or joint venture of any  kind between the parties.\n\n11.9 No Third-Party Beneficiaries.
    Source: 30
    Content: (b) if Google believes, in good faith, that the Distributor has violated or caused Google to violate any Anti-Bribery Laws (as  defined in Clause 8.5) or that such a violation is reasonably likely to occur,
    Source: 4
    =========
    FINAL ANSWER: {'has_answer': True, 'answer': 'This Agreement is governed by English law.', 'paragraphs': [28]}

    QUESTION: What did the president say about Michael Jackson?
    =========
    Content: Madam Speaker, Madam Vice President, our First Lady and Second Gentleman. Members of Congress and the Cabinet. Justices of the Supreme Court. My fellow Americans.  \n\nLast year COVID-19 kept us apart. This year we are finally together again. \n\nTonight, we meet as Democrats Republicans and Independents. But most importantly as Americans. \n\nWith a duty to one another to the American people to the Constitution. \n\nAnd with an unwavering resolve that freedom will always triumph over tyranny. \n\nSix days ago, Russia’s Vladimir Putin sought to shake the foundations of the free world thinking he could make it bend to his menacing ways. But he badly miscalculated. \n\nHe thought he could roll into Ukraine and the world would roll over. Instead he met a wall of strength he never imagined. \n\nHe met the Ukrainian people. \n\nFrom President Zelenskyy to every Ukrainian, their fearlessness, their courage, their determination, inspires the world. \n\nGroups of citizens blocking tanks with their bodies. Everyone from students to retirees teachers turned soldiers defending their homeland.
    Source: 0
    Content: And we won’t stop. \n\nWe have lost so much to COVID-19. Time with one another. And worst of all, so much loss of life. \n\nLet’s use this moment to reset. Let’s stop looking at COVID-19 as a partisan dividing line and see it for what it is: A God-awful disease.  \n\nLet’s stop seeing each other as enemies, and start seeing each other for who we really are: Fellow Americans.  \n\nWe can’t change how divided we’ve been. But we can change how we move forward—on COVID-19 and other issues we must face together. \n\nI recently visited the New York City Police Department days after the funerals of Officer Wilbert Mora and his partner, Officer Jason Rivera. \n\nThey were responding to a 9-1-1 call when a man shot and killed them with a stolen gun. \n\nOfficer Mora was 27 years old. \n\nOfficer Rivera was 22. \n\nBoth Dominican Americans who’d grown up on the same streets they later chose to patrol as police officers. \n\nI spoke with their families and told them that we are forever in debt for their sacrifice, and we will carry on their mission to restore the trust and safety every community deserves.
    Source: 24
    Content: And a proud Ukrainian people, who have known 30 years  of independence, have repeatedly shown that they will not tolerate anyone who tries to take their country backwards.  \n\nTo all Americans, I will be honest with you, as I’ve always promised. A Russian dictator, invading a foreign country, has costs around the world. \n\nAnd I’m taking robust action to make sure the pain of our sanctions  is targeted at Russia’s economy. And I will use every tool at our disposal to protect American businesses and consumers. \n\nTonight, I can announce that the United States has worked with 30 other countries to release 60 Million barrels of oil from reserves around the world.  \n\nAmerica will lead that effort, releasing 30 Million barrels from our own Strategic Petroleum Reserve. And we stand ready to do more if necessary, unified with our allies.  \n\nThese steps will help blunt gas prices here at home. And I know the news about what’s happening can seem alarming. \n\nBut I want you to know that we are going to be okay.
    Source: 5
    Content: More support for patients and families. \n\nTo get there, I call on Congress to fund ARPA-H, the Advanced Research Projects Agency for Health. \n\nIt’s based on DARPA—the Defense Department project that led to the Internet, GPS, and so much more.  \n\nARPA-H will have a singular purpose—to drive breakthroughs in cancer, Alzheimer’s, diabetes, and more. \n\nA unity agenda for the nation. \n\nWe can do this. \n\nMy fellow Americans—tonight , we have gathered in a sacred space—the citadel of our democracy. \n\nIn this Capitol, generation after generation, Americans have debated great questions amid great strife, and have done great things. \n\nWe have fought for freedom, expanded liberty, defeated totalitarianism and terror. \n\nAnd built the strongest, freest, and most prosperous nation the world has ever known. \n\nNow is the hour. \n\nOur moment of responsibility. \n\nOur test of resolve and conscience, of history itself. \n\nIt is in this moment that our character is formed. Our purpose is found. Our future is forged. \n\nWell I know this nation.
    Source: 34
    =========
    FINAL ANSWER: {'has_answer': False, 'answer': The president did not mention Michael Jackson., 'paragraphs': []}
    """,
    },
    {
        "role": "user",  # This one cannot be overriden
        "content": """QUESTION: {question}
    =========
    {summaries}
    =========
    FINAL ANSWER:""",
    },
]


class GenerativeQAWithSources(BaseModel):
    """Class handling the formatting and sending of the request.

    Parameters
    ----------
    client
        OpenAI or AsyncOpenAI client
    model
        OpenAI model to use for requests
    temperature
        Temperature of the model. controls its randomness
    max_tokens
        Maximum number of tokens the model will output
    """

    client: OpenAI | AsyncOpenAI
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int | None = None

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    def run(
        self,
        query: str,
        contexts: list[str],
        system_prompt: str | None = None,
    ) -> tuple[GenerativeQAOutput, str]:
        """Answer the question given the contexts.

        Parameters
        ----------
        query
            Question to answer.
        contexts
            Contexts to use to answer the question.
        system_prompt
            System prompt for the LLM. Leave None for default.

        Returns
        -------
        generated_text, finish_reason
            Answers to the question (in theory), reason for the LLM to stop.
        """
        # Put the documents in the prompt with the correct formats
        docs = self._process_retrieved_contexts(contexts)
        # Deep copying to avoid replacing completely the placeholders
        messages = copy.deepcopy(MESSAGES)
        if system_prompt:
            messages[0]["content"] = system_prompt
        messages[1]["content"] = messages[1]["content"].format(
            question=query, summaries=docs
        )

        # Run the chain.
        logger.info("Sending generative reader request.")
        if isinstance(self.client, OpenAI):
            response = self.client.beta.chat.completions.parse(
                messages=messages,  # type: ignore
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format=GenerativeQAOutput,
            )
        else:
            raise RuntimeError(
                "The OpenAI client might be an async one. Ensure that you are using a"
                " sync OpenAI client to call run."
            )
        finish_reason = response.choices[0].finish_reason
        logger.debug("Receiving generative reader request.")
        if isinstance(response.usage, CompletionUsage):
            logger.info(
                "Information about our OpenAI request:\n Input tokens:"
                f" {response.usage.prompt_tokens}\nOutput tokens:"
                f" {response.usage.completion_tokens}\nTotal tokens:"
                f" {response.usage.total_tokens}\nFinish reason: {finish_reason}"
            )
        output = response.choices[0].message.parsed
        return output, finish_reason  # type: ignore

    async def arun(
        self,
        query: str,
        contexts: list[str],
        system_prompt: str | None = None,
    ) -> tuple[GenerativeQAOutput, str]:
        """Answer the question given the contexts.

        Parameters
        ----------
        query
            Question to answer.
        contexts
            Contexts to use to answer the question.
        system_prompt
            System prompt for the LLM. Leave None for default.

        Returns
        -------
        generated_text, finish_reason
            Answers to the question (in theory), reason for the LLM to stop.
        """
        # Put the documents in the prompt with the correct formats.
        docs = self._process_retrieved_contexts(contexts)
        messages = copy.deepcopy(MESSAGES)
        if system_prompt:
            messages[0]["content"] = system_prompt
        messages[1]["content"] = messages[1]["content"].format(
            question=query, summaries=docs
        )

        # Run the chain.
        logger.info("Sending generative reader request.")
        if isinstance(self.client, AsyncOpenAI):
            response = await self.client.beta.chat.completions.parse(
                messages=messages,  # type: ignore
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format=GenerativeQAOutput,
            )
        else:
            raise RuntimeError(
                "The OpenAI client might be a sync one. Ensure that you are using a"
                " async AsyncOpenAI client to call arun."
            )
        finish_reason = response.choices[0].finish_reason
        logger.debug("Receiving generative reader request.")
        if isinstance(response.usage, CompletionUsage):
            logger.info(
                "Information about our OpenAI request:\n Input tokens:"
                f" {response.usage.prompt_tokens}\nOutput tokens:"
                f" {response.usage.completion_tokens}\nTotal tokens:"
                f" {response.usage.total_tokens}\nFinish reason: {finish_reason}"
            )
        output = response.choices[0].message.parsed
        return output, finish_reason  # type: ignore

    def stream(
        self,
        query: str,
        contexts: list[str],
        system_prompt: str | None = None,
    ) -> Generator[
        tuple[str, dict[str, bool | str | list[int]] | GenerativeQAOutput],
        None,
        str | None,
    ]:
        """Answer the question given the contexts.

        Parameters
        ----------
        query
            Question to answer.
        contexts
            Contexts to use to answer the question.
        system_prompt
            System prompt for the LLM. Leave None for default

        Yields
        ------
        chunks, parsed
            Chunks of the answer, (partially) parsed json.

        Returns
        -------
        finish_reason
            The reason for the LLM to stop generating.
        """
        # Put the documents in the prompt with the correct formats.
        docs = self._process_retrieved_contexts(contexts)
        messages = copy.deepcopy(MESSAGES)
        if system_prompt:
            messages[0]["content"] = system_prompt
        messages[1]["content"] = messages[1]["content"].format(
            question=query, summaries=docs
        )

        # Run the chain.
        logger.info("Sending generative reader request.")
        if not isinstance(self.client, OpenAI):
            raise RuntimeError(
                "The OpenAI client might be an async one. Ensure that you are using a"
                " sync OpenAI client to call stream."
            )
        finish_reason = None
        with self.client.beta.chat.completions.stream(
            messages=messages,  # type: ignore
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream_options={"include_usage": True},
            response_format=GenerativeQAOutput,
        ) as stream:
            for event in stream:
                # Inbetween chunks we have accumulated text -> skip
                if isinstance(event, ContentDeltaEvent):
                    continue
                # At the end we get the parsed pydantic class
                if isinstance(event, ContentDoneEvent):
                    if event.parsed is not None:  # mypy
                        yield "", event.parsed
                        continue

                if isinstance(event, ChunkEvent):  # mypy
                    # Only the last chunk contains the usage.
                    if not event.chunk.usage:
                        # case where a token is streamed
                        if event.chunk.choices[0].delta.content:
                            yield (  # type: ignore
                                event.chunk.choices[0].delta.content,
                                event.snapshot.choices[0].message.parsed,
                            )
                        else:
                            # No usage and no token -> finish reason is there.
                            # The first chunk might be empty and have no finish reason,
                            # it will be overriden later anyway.
                            finish_reason = event.chunk.choices[0].finish_reason
                    else:
                        logger.info(
                            "Information about our OpenAI request:\n Input tokens:"
                            f" {event.chunk.usage.prompt_tokens}\nOutput tokens:"
                            f" {event.chunk.usage.completion_tokens}\nTotal tokens:"
                            f" {event.chunk.usage.total_tokens}\nFinish reason: {finish_reason}"
                        )

                # In sync generators you can return a value, which will raise StopIteration and the returned
                # value can be retrieved as such:
                # ```python
                # gen = qas.stream(...)
                # try:
                #   while True:
                #       token = next(gen)
                # except StopIteration as err:
                #   finish_reason = err.value
                # ```
                if finish_reason:
                    return finish_reason
        return None  # for mypy

    async def astream(
        self,
        query: str,
        contexts: list[str],
        system_prompt: str | None = None,
    ) -> AsyncGenerator[
        tuple[str, dict[str, bool | str | list[int]] | GenerativeQAOutput], None
    ]:
        """Answer the question given the contexts.

        Parameters
        ----------
        query
            Question to answer.
        contexts
            Contexts to use to answer the question.
        system_prompt
            System prompt for the LLM. Leave None for default

        Yields
        ------
        chunks, parsed, finish_reason
            Answers to the question (in theory), partially parsed json. Final token is the reason for the LLM to stop.
        """
        # Put the documents in the prompt with the correct formats.
        docs = self._process_retrieved_contexts(contexts)
        messages = copy.deepcopy(MESSAGES)
        if system_prompt:
            messages[0]["content"] = system_prompt
        messages[1]["content"] = messages[1]["content"].format(
            question=query, summaries=docs
        )

        # Run the chain.
        logger.info("Sending generative reader request.")
        if not isinstance(self.client, AsyncOpenAI):
            raise RuntimeError(
                "The OpenAI client might be a sync one. Ensure that you are using a"
                " async AsyncOpenAI client to call astream."
            )
        finish_reason = None
        async with self.client.beta.chat.completions.stream(
            messages=messages,  # type: ignore
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream_options={"include_usage": True},
            response_format=GenerativeQAOutput,
        ) as stream:
            async for event in stream:
                # Inbetween chunks we have accumulated text -> skip
                if isinstance(event, ContentDeltaEvent):
                    continue
                # At the end we get the parsed pydantic class
                if isinstance(event, ContentDoneEvent):
                    if event.parsed is not None:  # mypy
                        yield "", event.parsed
                        continue

                if isinstance(event, ChunkEvent):  # mypy
                    # Only the last chunk contains the usage.
                    if not event.chunk.usage:
                        # case where a token is streamed
                        if event.chunk.choices[0].delta.content:
                            yield (  # type: ignore
                                event.chunk.choices[0].delta.content,
                                event.snapshot.choices[0].message.parsed,
                            )
                        else:
                            # No usage and no token -> finish reason is there.
                            # The first chunk might be empty and have no finish reason,
                            # it will be overriden later anyway.
                            finish_reason = event.chunk.choices[0].finish_reason
                    else:
                        logger.info(
                            "Information about our OpenAI request:\n Input tokens:"
                            f" {event.chunk.usage.prompt_tokens}\nOutput tokens:"
                            f" {event.chunk.usage.completion_tokens}\nTotal tokens:"
                            f" {event.chunk.usage.total_tokens}\nFinish reason: {finish_reason}"
                        )
        # It is considered a syntax error to return in an async iterator. This is a hack to do it anyway.
        if finish_reason:
            raise RuntimeError(finish_reason)

    @staticmethod
    def _process_retrieved_contexts(contexts: list[str]) -> str:
        """Process retrieved contexts.

        Parameters
        ----------
        contexts
            Contexts.

        Returns
        -------
        list[Document]
            Processed contexts.
        """
        # Potentially more post-processing if required, ex: splitting the text to reduce the number of tokens.
        contexts = [
            f"Content: {context}\nSource: {i}" for i, context in enumerate(contexts)
        ]
        documents = "\n".join(contexts)

        return documents
