from config.paths_config import *
from utils.helpers import *


def hybrid_recommendation(user_id, user_weight=0.5, content_weight=0.5):
    """
    Generates hybrid recommendations based on collaborative filtering and content-based similarity.

    Parameters:
    - user_id (int): The target user ID for whom recommendations are to be generated.
    - user_weight (float): Weight given to user-based recommendations.
    - content_weight (float): Weight given to content-based recommendations.

    Returns:
    - List[str]: A list of recommended anime names (strings).
    """

    # ---------- Collaborative Filtering ----------
    # Step 1: Find similar users
    similar_users = find_similar_users(
        item_input=user_id,
        path_user_weights=USER_WEIGHTS_PATH,
        path_user2user_encoded=USER2USER_ENCODED,
        path_user2user_decoded=USER2USER_DECODED,
    )

    # Step 2: Get high-rated anime preferences from the input user
    user_pref = get_user_preferences(
        user_id=user_id,
        path_rating_df=RATING_DF,
        path_anime_df=DF,
    )

    # Step 3: Recommend based on what similar users liked (but the user hasn't watched)
    user_recommended_animes = get_user_recommendations(
        similar_users=similar_users,
        user_pref=user_pref,
        path_anime_df=DF,
        path_synopsis_df=SYNOPSIS_DF,
        path_rating_df=RATING_DF,
    )

    # Extract anime names from user-based recommendations
    user_recommended_anime_list = user_recommended_animes["anime_name"].tolist()

    # ---------- Content-Based Filtering ----------
    content_recommended_animes = []

    for anime in user_recommended_anime_list:
        try:
            similar_animes_df = find_similar_animes(
                name=anime,
                path_anime_weights=ANIME_WEIGHTS_PATH,
                path_anime2anime_encoded=ANIME2ANIME_ENCODED,
                path_anime2anime_decoded=ANIME2ANIME_DECODED,
                path_anime_df=DF,
            )

            if similar_animes_df is not None and not similar_animes_df.empty:
                content_recommended_animes.extend(similar_animes_df["name"].tolist())

        except Exception as e:
            print(f"⚠️ Error finding similar animes for '{anime}':", e)

    # ---------- Combine & Score ----------
    combined_scores = {}

    # Score user-based recommendations
    for anime in user_recommended_anime_list:
        combined_scores[anime] = combined_scores.get(anime, 0) + user_weight

    # Score content-based recommendations
    for anime in content_recommended_animes:
        combined_scores[anime] = combined_scores.get(anime, 0) + content_weight

    # Sort by score in descending order
    sorted_animes = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)

    # Return top 10 anime names
    return [anime for anime, _ in sorted_animes[:10]]
