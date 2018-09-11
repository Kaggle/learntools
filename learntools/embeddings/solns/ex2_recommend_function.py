def recommend(model, user_id, n=5):
    all_movie_ids = movies.index
    preds = model.predict([
        np.repeat(uid, len(all_movie_ids)),
        all_movie_ids,
    ])
    # Add back the offset calculated earlier, to 'uncenter' the ratings, and get back to a [0.5, 5] scale.
    movies.loc[all_movie_ids, 'predicted_rating'] = preds + offset
    reccs = movies.sort_values(by='predicted_rating', ascending=False).head(n)
    return reccs
