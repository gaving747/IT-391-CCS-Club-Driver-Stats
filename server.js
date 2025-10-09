import express from "express";
import XLSX from "xlsx";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());

const PORT = process.env.PORT || 3000;
const EXCEL_PATH = path.join(__dirname, "race_data.xlsx");

app.get("/api/results", (req, res) => {
  try {
    const workbook = XLSX.readFile(EXCEL_PATH);
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const data = XLSX.utils.sheet_to_json(sheet);
    res.json(data);
  } catch (err) {
    console.error("Error reading Excel file:", err);
    res.status(500).json({ error: "Failed to read race data" });
  }
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/api/results`);
});
