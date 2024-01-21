import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# ini collaborative menggunakan user-id 122
with open('collab1.pkl', 'rb') as file:
    loaded_data_fix = pickle.load(file)

# datafix = loaded_data_fix.pivot_table(index='User-ID', columns='Produk', values='Rating').fillna(0)
# Hitung rata-rata prediksi untuk setiap pengguna
user_avg_ratings = loaded_data_fix.mean(axis=1)

# Rangking pengguna berdasarkan rata-rata prediksi
ranked_users = user_avg_ratings.sort_values(ascending=False)

# Rekomendasi Top-N untuk satu pengguna (peringkat teratas)
N = 10  # Ganti N dengan jumlah item yang ingin direkomendasikan

# Pilih satu pengguna dengan peringkat teratas
user_idx_to_display = ranked_users.index[0]

# Rekomendasi Top-N untuk satu pengguna
top_n_recommendations = loaded_data_fix.loc[user_idx_to_display].sort_values(ascending=False).head(8)

print(f"Rekomendasi untuk User-idx {user_idx_to_display}:")
for item_idx in top_n_recommendations.index:
        print(f"{item_idx}")







#ini hybrid menggunakan user id 1
datasetCb = pd.read_csv('datacontent-id.csv') #ini load data content based
with open('data_train.pkl', 'rb') as train:
    loaded_data_train = pickle.load(train) #ini load data_train.pkl dari collaborative
with open('data_test.pkl', 'rb') as test:
    loaded_data_test = pickle.load(test) #ini load data_test.pkl dari collaborative

#ini cosine sim untuk prediksi collab
def cosineSimilarity(ratings_matrix, u, v):
    ratings_u = ratings_matrix[:, u]
    ratings_v = ratings_matrix[:, v]
    dot_product = np.nansum(ratings_u * ratings_v)
    norm_u = np.sqrt(np.nansum(ratings_u**2))
    norm_v = np.sqrt(np.nansum(ratings_v**2))

    if norm_u == 0.0 or norm_v == 0.0 or np.isnan(norm_u) or np.isnan(norm_v):
        similarity = 0.0
    else:
        similarity = dot_product / (norm_u * norm_v)

    return similarity

#ini prediksi collab
def prediksi_rating(user_id, loaded_data_train, item_ratingTrain, item_ratingTest):
    if user_id >= loaded_data_train.shape[0]:
        raise ValueError("Invalid User-ID")

    predicted_ratings = []
    for item_id in item_ratingTest:
        weighted_sum = 0
        total_similarity = 0

        for item in item_ratingTrain:
            similarity = cosineSimilarity(loaded_data_train, item_id, item)
            rating_train = loaded_data_train[user_id, item]
            weighted_sum += similarity * rating_train
            total_similarity += similarity

        if total_similarity != 0:
            predicted_rating = weighted_sum / total_similarity
            predicted_ratings.append(predicted_rating)
        else:
            predicted_ratings.append(np.nan)

    return np.array(predicted_ratings)

#ini untuk user id 1
user_id = 1
#ini untuk ambil data train yang dirating berdasarkan user id-0
item_ratingTrain = np.where((~np.isnan(loaded_data_train[user_id, :])) & (loaded_data_train[user_id, :] >= 1) & (loaded_data_train[user_id, :] <= 5))[0]
item_ratingTest = np.where((~np.isnan(loaded_data_test[user_id, :])) & (loaded_data_test[user_id, :] >= 1) & (loaded_data_test[user_id, :] <= 5))[0]
#ini fungsi content based
features = ['Tipe Motor', 'Jenis Ban', 'Ukuran Ban', 'Harga']
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder())])
numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, ['Harga']),
        ('cat', categorical_transformer, ['Tipe Motor', 'Jenis Ban', 'Ukuran Ban'])
    ])

X = preprocessor.fit_transform(datasetCb[features])
cosine_sim_matrix = cosine_similarity(X, X)
def recommend_motor(input_jenis_motor, input_jenis_ban, input_ukuran_ban, input_harga, cosine_sim_matrix, motor_data, top_n = len(item_ratingTest)):
    input_data = pd.DataFrame({
        'Tipe Motor': [input_jenis_motor],
        'Jenis Ban': [input_jenis_ban],
        'Ukuran Ban': [input_ukuran_ban],
        'Harga': [input_harga]
    })

    input_vector = preprocessor.transform(input_data)

    sim_scores = cosine_similarity(input_vector, X)
    sim_scores = list(enumerate(sim_scores[0]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_n_motor = sim_scores[:top_n]

    return top_n_motor

input_jenis_motor = 'Matic'
input_jenis_ban = 'Tubeless Tire'
input_ukuran_ban = '80/90-14'
input_harga = 200000

recommended_motor = recommend_motor(input_jenis_motor, input_jenis_ban, input_ukuran_ban, input_harga, cosine_sim_matrix, datasetCb)
cosine_scores = [score for _, score in recommended_motor]
weighted_scores = [score for score in cosine_scores]

# Step 1: Get Content-Based Recommendations
content_based_recommendations = weighted_scores
print(content_based_recommendations)
# Step 2: Get Collaborative Recommendations
prediction = prediksi_rating(user_id, loaded_data_train, item_ratingTrain, item_ratingTest)

# Step 4: Combine Content-Based and Collaborative Scores
hybrid_score = 0.7 * np.array(content_based_recommendations) + 0.3 * prediction

# Display Hybrid Recommendations
print("Hybrid Recommendations:", hybrid_score)

print("Hybrid Recommendations (Hybrid Score):", hybrid_score)

top_n_indices = np.argsort(hybrid_score)[::-1][:15]

top_n_products = datasetCb.iloc[top_n_indices]
top_n_product_names = top_n_products['Nama Produk']
top_n_product_ukuran = top_n_products['Ukuran Ban']

print("Top N Recommended Products Hybrid:")
print(top_n_product_names, top_n_product_ukuran)
