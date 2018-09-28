def recommend_nonobscure(model, user_id, n=5, min_ratings=1000):
    # Add predicted_rating column if we haven't already done so.
    if 'predicted_rating' not in movies.columns:
        all_movie_ids = df.movieId.unique()
        preds = model.predict([
            np.repeat(uid, len(all_movie_ids)),
            all_movie_ids,
        ])
        # Add back the offset calculated earlier, to 'uncenter' the ratings, and get back to a [0.5, 5] scale.
        movies.loc[all_movie_ids, 'predicted_rating'] = preds + offset
    
    nonobscure_movie_ids = movies.index[movies.n_ratings >= min_ratings]
    return movies.loc[nonobscure_movie_ids].sort_values(by='predicted_rating', ascending=False).head(n)
