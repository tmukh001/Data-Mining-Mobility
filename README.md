# 📍 Urban Mobility Mining: Apriori, GSP, and LSTM Approaches

A comprehensive project applying **unsupervised learning**, **sequential pattern mining**, and **neural networks** to discover mobility trends and predict future locations based on city trajectory data. Completed as part of the *SC4020: Data Analytics and Mining* course at NTU Singapore.

---

## 🧭 Project Overview

This repository includes 3 major components:

### 1. 🔄 Apriori Algorithm – Co-Occurrence of POIs
- Analyzes which **Points of Interest (POIs)** frequently appear together in the same spatial grid across four cities.
- Implements custom candidate generation, pruning, and support counting from scratch.
- Input: POI distribution data per city  
- Output: Frequent POI itemsets for varying support thresholds

### 2. 📈 Sequential Pattern Mining – GSP Algorithm
- Extracts **common movement patterns** from user trip sequences.
- Uses **Generalized Sequential Pattern (GSP)** mining to find frequent subsequences from user triplegs.
- Data is first cleaned, filtered, and transformed into sequences of geographic coordinates.

### 3. 🤖 LSTM-based Prediction – Predicting Next Location
- Builds separate **LSTM models per city** to predict the next location from past trajectories.
- Trained on fixed-length subsequences from user triplegs.
- Evaluates results using **Mean Squared Error (MSE)** and visualizes prediction errors.

---

## 📊 Key Results

| Task               | Summary Result |
|--------------------|----------------|
| **Apriori**         | Found frequent POI co-occurrence patterns across cities with support thresholds 0.15–0.4 |
| **GSP**             | Extracted top 10 movement subsequences per city from tripleg data |
| **LSTM**            | Achieved test MSEs: A – 76.84, B – 58.36, C – 53.59, D – 57.58 |

---

## 📚 Technologies Used

- Python  
- Pandas, NumPy  
- scikit-learn  
- TensorFlow / Keras  
- Matplotlib  
- GeoPandas (for tripleg processing)  

---

## 👨‍💻 Contributors
Lim Jun Yu         
Poh Zi Jie Isaac     
Dexter Voon Kai Xian  
**Tathagato Mukherjee**

---
