import os
import operator
import requests
import asyncio
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from typing import TypedDict,Annotated
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatMistralAI(model_name="mistral-small-2506",temperature=0.85)


class Movie(TypedDict):
    User_input : str
    Movie_details : dict
    Movie_Finder : str
    Review_Analyzer : Annotated[str, operator.add]
    OTT_checker : Annotated[str, operator.add]
    Recommendation : str


def Movie_details(state: Movie):

    movie = state["User_input"]
    API_KEY = "b21563d1"

    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={movie}"

    response = requests.get(url)
    movie = response.json()

    if movie["Response"] == "False":
       raise ValueError("Movie not found")
    
    return {
    "Movie_details": {
        "Title": movie.get("Title"),
        "Release Year": movie.get("Year"),
        "Genre": movie.get("Genre"),
        "Runtime": movie.get("Runtime"),
        "Director": movie.get("Director"),
        "Cast": movie.get("Actors"),
        "IMDB Rating": movie.get("imdbRating"),
        "Plot": movie.get("Plot"),
        "BoxOffice": movie.get("BoxOffice"),
        "Language": movie.get("Language"),
    }
}




async def Movie_Finder(state:Movie) -> dict:
    print("\n Agent [1] It finds the Relevant Movies from the which is getted from the past movie uploaded")
 
    movie = state["Movie_details"]

    
    prompt = (
        f"""
        You are an expert movie recommendation assistant.

        Based on the following movie details, recommend 10 similar movies or TV series.

        Movie Details:
        Title: {movie['Title']}
        Genre: {movie['Genre']}
        IMDb Rating: {movie['IMDB Rating']}
        Language: {movie['Language']}
        Plot: {movie['Plot']}

        Instructions:
        1. Recommend only similar movies or TV series.
        2. Consider the genre, storyline, themes, and mood.
        3. Do not recommend the same movie.
        4. Prefer highly rated and popular titles.
        5. Return exactly 10 recommendations.
        """

    )
    
    response = await llm.ainvoke(prompt)
    print(response.content)
    return {"Movie_Finder":response.content}





async def Review_Analyzer(state:Movie) -> dict:
    print("\n Agent [2] It explains why it matches the recommeded movie from the given movie")
    
    movie = state["Movie_details"]

    prompt = ( f"""
            You are an expert movie analyst.

            Original Movie:
            Title: {movie['Title']}
            Genre: {movie['Genre']}
            Language: {movie['Language']}
            Plot: {movie['Plot']}

            Recommended Movies:
            {state["Movie_Finder"]}

            For each recommended movie, explain why it is similar to the original movie.

            Compare based on:
            - Genre
            - Storyline
            - Themes
            - Mood
            - Main Characters
            - Audience Appeal

            Return the response in the following format:

            Movie: <Movie Name>

            Similarity Score: <0-100%>

            Genre Match:
            <Explain>

            Storyline Match:
            <Explain>

            Theme Match:
            <Explain>

            Mood Match:
            <Explain>

            Audience Appeal:
            <Explain>

            """
    )
    response = await llm.ainvoke(prompt)
    print(response.content)
    return {"Review_Analyzer":response.content}




async def Recommendation(state:Movie) -> dict:
    print("\n Agent [3] It Recommends the Top 5 Movies from the generated the from Top 20 movies which are mostly impressed and good")

    movie = state["Movie_details"]

    prompt = (f"""
        You are an expert movie recommendation assistant.

        Original Movie:
        Title: {movie['Title']}
        Genre: {movie['Genre']}
        Language: {movie['Language']}
        Plot: {movie['Plot']}

        Recommended Movies and Analysis:
        {state["Review_Analyzer"]}

        OTT Availability:
        {state["OTT_checker"]}

        Select the best 3 movies from the recommendations.

        Rank them based on:
        - Similarity to the original movie
        - Genre match
        - Storyline
        - Themes
        - Audience appeal
        - IMDb Rating

        Return the response in the following format:

        🏆 Rank 1
        Movie:
        IMDb Rating:
        Why it is the Best Choice:

        ----------------------------

        🥈 Rank 2
        Movie:
        IMDb Rating:
        Why it is Recommended:

        ----------------------------

        🥉 Rank 3
        Movie:
        IMDb Rating:
        Why it is Recommended:
        """
    )
    response = await llm.ainvoke(prompt)
    print(response.content)
    return {"Recommendation":response.content}



async def OTT_checker(state:Movie) -> dict:
    print("\n Agent[4] It gives where to watch this movies and where can see those movies in the socail media or apps or OTT platforms")
    movie = state["Movie_Finder"]

    prompt = (f"""
        You are an expert movie streaming assistant.

        The user has selected the following top 3 recommended movies:

        {state["Movie_Finder"]}

        Your task is to identify where each movie or TV series is available to watch.

        For each movie provide:

        Movie:
        Available On:
        Platform(s):
        Subscription Type (Free / Subscription / Rent / Buy):
        Region (if known):

        If the movie is not available on any OTT platform, mention:
        "Currently unavailable for streaming."

        Return the response in the following format:

        🎬 Movie:
        Available On:
        Subscription:
        Region:

        ----------------------------------
        """
    )
    response = await llm.ainvoke(prompt)
    print(response.content)
    return {"OTT_checker":response.content}




builder = StateGraph(Movie)

builder.add_node("movie_details",Movie_details)
builder.add_node("movie_finder",Movie_Finder)
builder.add_node("review_analyzer",Review_Analyzer)
builder.add_node("recommendation",Recommendation)
builder.add_node("ott_checker",OTT_checker)

builder.add_edge(START, "movie_details")
builder.add_edge("movie_details", "movie_finder")
builder.add_edge("movie_finder", "review_analyzer")
builder.add_edge("movie_finder", "ott_checker")
builder.add_edge("review_analyzer", "recommendation")
builder.add_edge("ott_checker", "recommendation")
builder.add_edge("recommendation", END)


app = builder.compile()

if __name__ == "__main__":
    movie_you_entered = input("Enter the Movie Name / TV Show : ")

    workflow = {
        "User_input": movie_you_entered,
    }

    final = asyncio.run(app.ainvoke(workflow))

    print(final["Movie_details"])
    print(final["Movie_Finder"])
    print(final["Review_Analyzer"])
    print(final["Recommendation"])
    print(final["OTT_checker"])