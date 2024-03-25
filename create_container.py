### This file should be put into the main directory of the repository that contains the movie recommendation model code. ###

from src.user_based_model_optim import UserBasedRecommendationModel
from chassisml import ChassisModel
from chassis.builder import DockerBuilder

# Load pre-trained model
model = UserBasedRecommendationModel(model_path="user-based-trained.pkl",
                                     data_path="data-cleaning/cleaned-movie-data-train-movieid.csv",
                                     max_recommendation_count=20)

# Define predict function
def predict(input_bytes):
    user_id = input_data['input'].decode()
    recommendations = model.get_recommendations(int(user_id))
    recommendations = ','.join(recommendations)
    output = {
        "data": {
            "result": {"recommendations": recommendations}
        }
    }
    return {'results.json': json.dumps(output).encode()}

# Build Chassis model
chassis_model = ChassisModel(process_fn=predict)
# Add Python libraries that are needed to run the model
chassis_model.add_requirements(["pandas", "surprise", "tqdm"])
# Add metadata
chassis_model.metadata.model_name = "User-Based CF Movie Recommendations"
chassis_model.metadata.model_version = "0.0.1"
chassis_model.metadata.add_input(
    key="input",
    accepted_media_types=["text/plain"],
    max_size="10M",
    description="User ID as a string"
)
chassis_model.metadata.add_output(
    key="results.json",
    media_type="application/json",
    max_size="1M",
    description="List of top 20 recommended movie names"
)

# Build Docker image
builder = DockerBuilder(chassis_model)
start_time = time.time()
res = builder.build_image(name="user-based-cf", tag="0.0.1", show_logs=True)
end_time = time.time()
print(res)
print(f"Container image built in {round((end_time-start_time)/60, 5)} minutes")
