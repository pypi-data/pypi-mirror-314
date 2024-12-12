import requests
import pickle
import base64
import numpy as np

class ModelUploader:
    def __init__(self, api_key):
        self.api_key = api_key
        self.server_url = "https://viturka.com/upload_model"

    def pad_to_match_shape(self, model1_weights, model2_weights):
        """Pad the smaller array with zeros to match the size of the larger one."""
        if len(model1_weights) > len(model2_weights):
            padded_model2 = np.pad(model2_weights, (0, len(model1_weights) - len(model2_weights)), 'constant')
            return model1_weights, padded_model2
        elif len(model2_weights) > len(model1_weights):
            padded_model1 = np.pad(model1_weights, (0, len(model2_weights) - len(model1_weights)), 'constant')
            return padded_model1, model2_weights
        else:
            return model1_weights, model2_weights

    def upload_model(self, model, model_type, vectorizer= None):
        # Serialize the local model
        model_data = pickle.dumps(model)
        if vectorizer:
            v_data = pickle.dumps(vectorizer)
        else:
            v_data = None

        # Send the model to the server and receive the global model
        response = requests.post(
            f'{self.server_url}',
            files={'model': ('model.pkl', model_data, 'application/octet-stream'), 'vectorizer': (f'{model_type}_vectorizer.pkl', v_data, 'application/octet-stream')},
            data={'api_key': self.api_key, 'model_type': model_type}
        )

        if response.status_code == 200:
            # Deserialize the received global model
            data = response.json()
            if data['model'] == 200:
                global_model = model
            else:
                # Decode the base64 encoded string back to bytes
                pickled_model = base64.b64decode(data['model'])

                # Unpickle the model
                global_model = pickle.loads(pickled_model)

            # Perform local aggregation
            model.w_, global_model.w_ = self.pad_to_match_shape(model.w_, global_model.w_)

            # Update w_ (Linear Coefficients)
            for i in range(len(model.w_)):
                if global_model.w_[i] != 0 and model.w_[i] != 0:
                    model.w_[i] = (model.w_[i] + global_model.w_[i]) / 2  # Average for shared features
                else:
                    model.w_[i] += global_model.w_[i]  # Directly add non-shared features

            # Align V_ matrices and aggregate (if V_ is a matrix, align by rows/columns)
            max_rows = max(model.V_.shape[0], global_model.V_.shape[0])
            max_cols = max(model.V_.shape[1], global_model.V_.shape[1])

            padded_model_V = np.pad(model.V_,
                                    ((0, max_rows - model.V_.shape[0]), (0, max_cols - model.V_.shape[1])),
                                    'constant')
            padded_global_V = np.pad(global_model.V_,
                                     ((0, max_rows - global_model.V_.shape[0]),
                                      (0, max_cols - global_model.V_.shape[1])),
                                     'constant')

            # Update V_ (Latent Factor Matrix)
            for row in range(padded_model_V.shape[0]):
                for col in range(padded_model_V.shape[1]):
                    if padded_model_V[row, col] != 0 and padded_global_V[row, col] != 0:
                        padded_model_V[row, col] = (padded_model_V[row, col] + padded_global_V[row, col]) / 2
                    else:
                        padded_model_V[row, col] += padded_global_V[row, col]

            model.V_ = padded_model_V

            # Aggregate bias term w0_
            model.w0_ = (model.w0_ + global_model.w0_) / 2

            print("Model uploaded and aggregated successfully.")
        else:
            print(f"Failed to upload model: {response.content.decode()}")

        return model


