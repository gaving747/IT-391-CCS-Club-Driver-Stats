# Champaign County Sports Car Club Race Data API

This Node.js project provides an API endpoint to access autocross race data stored in an Excel file.

## 🚀 Features
- Reads Excel data using the `xlsx` package
- Serves data as JSON at `/api/results`
- Cross-origin enabled for use with your dashboard frontend

## ⚙️ Setup Instructions
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ccscc-race-api.git
   cd ccscc-race-api
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Place your Excel file in the root folder and name it:
   ```
   race_data.xlsx
   ```

4. Run the server:
   ```bash
   npm start
   ```

5. Access your API at:
   ```
   http://localhost:3000/api/results
   ```

## 📦 Example JSON Output
```json
[
  {
    "Driver": "John Doe",
    "Car": "Mazda Miata",
    "Raw Time": 46.28,
    "PAX Time": 39.42,
    "Penalties": 0
  }
]
```
