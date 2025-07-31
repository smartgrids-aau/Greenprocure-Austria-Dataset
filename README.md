# Dataset and Python code for analyzing CO₂ emissions in public procurement to identify sustainable strategies in southern Austria

This repository contains municipal procurement data from southern Austria along with a comprehensive analysis tool for identifying sustainable purchasing strategies through statistical classification and carbon footprint assessment as a supplement to our research paper "Identifying Sustainable Procurement Pathways: A Case Study
Using ABC and XYZ Analyses in Southern Austria" (submitted).

## Repository Structure

```
├── dataset/                  # Municipal procurement data
├── GreenProcureAnalyzer/     # Analysis tool and source code
├── Output/                   # Generated reports and graphs
└── README.md
```

---

## 📊 Dataset

The `dataset/` folder contains real-world procurement data from municipalities in southern Austria, providing insights into public sector purchasing patterns across different product categories.

### Data Coverage
- **Geographic Scope**: Southern Austria municipalities
- **Product Categories**: 
  - Treibstoffe (Fuels)
  - Verbrauchsgüter (Consumables) 
  - Gebrauchsgüter (Reusables)
- **Data Fields**: Product descriptions, costs, purchase dates, quantities
- **Format**: Excel/CSV files with structured procurement records

### Research Applications
This dataset enables analysis of:
- Municipal spending patterns and budget allocation
- Seasonal procurement trends
- Carbon footprint patterns in public sector purchasing
- Cost optimization opportunities in government procurement
- Sustainability benchmarking across different municipalities

---

## 🔧 GreenProcureAnalyzer Tool

The `GreenProcureAnalyzer/` folder contains a comprehensive Python-based analytics tool that processes municipal procurement data to provide actionable insights for sustainable purchasing decisions.

### Core Features

**Statistical Classification**
- **ABC Analysis**: Classifies items by cost importance (A=high value, B=medium value, C=low value)
- **XYZ Analysis**: Classifies items by demand predictability (X=predictable, Y=moderate variation, Z=unpredictable)

**Environmental Impact Assessment**
- **CO₂ Footprint Tracking**: Calculates carbon equivalent emissions for all purchases
- **Sustainability Reporting**: Generates environmental impact reports by product category
- **Timeline Analysis**: Tracks emission trends over time

**Advanced Analytics**
- Coefficient of variation calculations for demand forecasting
- Multi-category analysis across fuel, consumable, and reusable products
- Automated Excel report generation with visualizations

### Quick Start

#### Prerequisites
- Python 3.7+ with packages: `pandas`, `matplotlib`, `seaborn`

#### Usage
1. **Setup Data**
   ```bash
   cd GreenProcureAnalyzer/
   # Place procurement data in dataset/ folder (already included)
   ```

2. **Configure Analysis**
   ```python
   # Edit config.py to set analysis timeframe
   MIN_YEAR = 2022
   MAX_YEAR = 2024
   ```

3. **Run Analysis**
   ```bash
   python run.py
   ```

4. **View Results**
   - Generated reports saved in `output/` folder
   - Includes ABC/XYZ classifications, CO₂ analysis, and timeline trends

#### Configuration
Create JSON files in `tables/` folder to define data structure:
```json
{
  "table": "municipality_data",
  "columns": {
    "Products": "product_name",
    "Cost": "total_cost", 
    "Date": "purchase_date"
  },
  "dateformat": "%Y-%m-%d",
  "outputcolumns": ["product_name", "total_cost", "quantity"]
}
```

### Output Reports
- **ABC Classification**: Cost-based importance ranking
- **XYZ Timeline Analysis**: Demand variability patterns over time  
- **CO₂ Impact Assessment**: Carbon footprint analysis by category
- **Integrated Sustainability Reports**: Combined cost and environmental insights

---

