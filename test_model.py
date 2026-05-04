import pickle
import numpy as np

with open('model/model.pkl', 'rb') as f:
    payload = pickle.load(f)
    model = payload['model']
    scaler = payload['scaler']
    print('✓ Model loaded successfully')
    print(f'✓ Model type: {type(model).__name__}')
    print(f'✓ Feature names: {payload.get("feature_names", [])}')
    
# Test prediction
test_data = np.array([[6, 250, 150, 3500, 15, 75, 1]])
test_scaled = scaler.transform(test_data)
pred = model.predict(test_scaled)
print(f'✓ Test prediction successful: {pred[0]:.2f} MPG')
