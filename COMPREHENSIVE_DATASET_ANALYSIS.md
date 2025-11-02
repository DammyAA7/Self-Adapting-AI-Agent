# Comprehensive Dataset Analysis

**Self-Adapting AI Agent Framework - Complete Codebase Analysis**

**Generated:** 2025-10-12
**Location:** `/mnt/c/Users/User/PycharmProjects/new_code/Self-Adapting-AI-Agent/dataset/`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Dataset-by-Dataset Analysis](#2-dataset-by-dataset-analysis)
3. [Comparative Analysis](#3-comparative-analysis)
4. [Technical Specifications](#4-technical-specifications)
5. [Appendix: Summary Tables](#5-appendix-summary-tables)

---

## 1. Overview

### 1.1 Executive Summary

This repository contains **11 distinct datasets** organized for testing a self-adapting AI agent system. The datasets span multiple domains (healthcare, education, HR analytics, e-commerce, media recommendation, social networks, IoT, mathematics, and finance) with varying complexity levels from minimal cross-session problems to fully-implemented multi-class systems.

### 1.2 Global Statistics

| Metric | Value |
|--------|-------|
| **Total Datasets** | 11 |
| **Total Python Files** | 48 |
| **Total Classes** | 49 |
| **Total Methods/Functions** | 195+ |
| **Total Lines of Code (Python)** | 2,685 |
| **Data Files (CSV/JSON)** | 4 |
| **Data File Lines** | 3,152 |

### 1.3 Dataset Classification

#### Code-Heavy Datasets (4)
1. **patient_risk_analyzer** - 12 Python files, 20 classes, 740 LOC
2. **student_gpa_calculator** - 10 Python files, 10 classes, 773 LOC
3. **salary_analyzer** - 13 Python files, 12 classes, 603 LOC
4. **inventory_replenishment** - 8 Python files, 7 classes, 569 LOC

#### Data-Only Datasets (4)
5. **book_recommender** - CSV data (100 books)
6. **friend_suggester** - JSON data (100 users, social network)
7. **movielens_dataset** - CSV data (100 movies)
8. **performance_tracker** - CSV data (50 employee reviews)

#### Minimal/Cross-Session Datasets (3)
9. **iot_sensor_pipeline** - Minimal stub (5 LOC)
10. **matrix_eigenvalue_composition** - Minimal stub (5 LOC)
11. **portfolio_risk_calculator** - Minimal stub (5 LOC)

---

## 2. Dataset-by-Dataset Analysis

### 2.1 Patient Risk Analyzer

**Location:** `/dataset/patient_risk_analyzer/`

#### A. Basic Information
- **Dataset ID:** 2
- **Domain:** Healthcare
- **Purpose:** Calculate patient risk scores based on age, medical conditions, vital signs, and medical history
- **Task Type:** Function implementation with complex medical domain logic
- **Entry Point:** `patient_risk_score()`

#### B. Code Structure Analysis

**Python Files (12):**
1. `__init__.py` (39 LOC) - Package initialization and exports
2. `patient.py` (34 LOC) - Core patient data model
3. `condition.py` (17 LOC) - Medical condition representation
4. `medical_record.py` (30 LOC) - Visit records with vitals
5. `hospital.py` (94 LOC) - Hospital management system
6. `medication_manager.py` (77 LOC) - Drug management
7. `vital_signs_analyzer.py` (88 LOC) - Vital signs processing
8. `appointment_scheduler.py` (60 LOC) - Appointment management
9. `insurance_processor.py` (75 LOC) - Insurance handling
10. `lab_results.py` (70 LOC) - Laboratory test management
11. `diagnosis_helper.py` (79 LOC) - Diagnostic utilities
12. `treatment_plan.py` (77 LOC) - Treatment planning

**Total Lines of Code:** 740

**Classes (20):**
- **Core Models:** `Patient`, `Condition`, `MedicalRecord`, `Hospital`
- **Medication System:** `Medication`, `DrugInteractionChecker`, `DosageCalculator`
- **Vital Signs:** `VitalSignsTrends`, `HeartRateMonitor`
- **Appointments:** `Appointment`, `AppointmentScheduler`
- **Insurance:** `InsurancePlan`, `InsuranceVerifier`, `ClaimProcessor`
- **Laboratory:** `LabTest`, `LabResultsManager`
- **Diagnosis:** `SymptomChecker`, `DiagnosticCriteria`
- **Treatment:** `TreatmentPlan`, `CareProtocol`

**Key Methods (59 total):**
- `Patient.add_condition()` - Add medical condition
- `Patient.get_total_conditions()` - Count conditions
- `Patient.get_average_severity()` - Calculate average severity
- `Hospital.get_patient()` - Retrieve patient by ID
- `Hospital.get_recent_records()` - Get records within timeframe
- `MedicalRecord.has_abnormal_vitals()` - Check vital sign ranges
- `create_sample_hospital()` - Generate test data

#### C. Data Files
**None** - Uses programmatically generated test data

#### D. Module Architecture

**Import Dependencies:**
```python
patient.py → condition.py
hospital.py → patient.py, medical_record.py, condition.py
All helper modules → core models
```

**Package Exports:**
```python
__all__ = [
    # Core classes
    'Condition', 'Patient', 'MedicalRecord', 'Hospital', 'create_sample_hospital',
    # 15 additional helper classes
]
```

#### E. Complexity Metrics
- **Classes:** 20
- **Methods:** 59
- **Cyclomatic Complexity:** Medium-High (medical business logic)
- **Integration Complexity:** High (20 interrelated classes)
- **Domain Complexity:** High (healthcare domain knowledge required)

**Risk Score Calculation Formula:**
```
risk_score = (age/100 * 30)
           + (total_conditions * 5 * 0.25)
           + (avg_severity * 10 * 0.25)
           + (20 if abnormal_vitals else 0)
```

---

### 2.2 Student GPA Calculator

**Location:** `/dataset/student_gpa_calculator/`

#### A. Basic Information
- **Dataset ID:** 3
- **Domain:** Education
- **Purpose:** Calculate student GPA from course enrollments and grades
- **Task Type:** Academic computation with grade point system
- **Entry Point:** `calculate_simple_gpa()`

#### B. Code Structure Analysis

**Python Files (10):**
1. `__init__.py` (22 LOC) - Package initialization
2. `student.py` (16 LOC) - Student model
3. `course.py` (20 LOC) - Course definition
4. `enrollment.py` (26 LOC) - Student-course enrollment
5. `department.py` (15 LOC) - Academic department
6. `university.py` (127 LOC) - University system with sample data
7. `grade_calculator.py` (107 LOC) - Grade computation logic
8. `transcript_generator.py` (122 LOC) - Academic transcripts
9. `prerequisite_checker.py` (150 LOC) - Course prerequisites
10. `scholarship_evaluator.py` (168 LOC) - Scholarship evaluation

**Total Lines of Code:** 773

**Classes (10):**
- **Core Models:** `Student`, `Course`, `Enrollment`, `Department`, `University`
- **Utilities:** `GradeCalculator`, `TranscriptGenerator`, `PrerequisiteChecker`, `ScholarshipEvaluator`
- **Enums:** `ScholarshipType`

**Key Methods (43 total):**
- `Enrollment.get_grade_points()` - Convert letter grade to points
- `University.get_student_enrollments()` - Get student's courses
- `University.get_course()` - Retrieve course by code
- `GradeCalculator.calculate_gpa()` - GPA computation
- `TranscriptGenerator.generate_transcript()` - Create academic record
- `PrerequisiteChecker.check_prerequisites()` - Validate course eligibility
- `ScholarshipEvaluator.evaluate_eligibility()` - Scholarship assessment
- `create_sample_university()` - Generate test data

#### C. Data Files
**None** - Uses programmatically generated test data

#### D. Module Architecture

**Import Dependencies:**
```python
enrollment.py → course.py, student.py
university.py → student.py, course.py, enrollment.py, department.py
Helper classes → core models
```

**Package Exports:**
```python
__all__ = [
    'Course', 'Enrollment', 'Student', 'Department', 'University',
    'GradeCalculator', 'TranscriptGenerator', 'PrerequisiteChecker',
    'ScholarshipEvaluator', 'ScholarshipType', 'create_sample_university'
]
```

#### E. Complexity Metrics
- **Classes:** 10
- **Methods:** 43
- **Cyclomatic Complexity:** Medium (academic rules and calculations)
- **Integration Complexity:** Medium (10 classes, hierarchical)
- **Domain Complexity:** Medium (GPA calculation, grade system)

**GPA Calculation Formula:**
```
GPA = sum(grade_points * credits) / sum(credits)
```

**Grade Point Scale:**
- A = 4.0, A- = 3.7, B+ = 3.3, B = 3.0, B- = 2.7, C+ = 2.3, C = 2.0, D = 1.0, F = 0.0

---

### 2.3 Salary Analyzer

**Location:** `/dataset/salary_analyzer/`

#### A. Basic Information
- **Dataset ID:** 1
- **Domain:** HR Analytics
- **Purpose:** Analyze and calculate average salary from employee database
- **Task Type:** Data processing and statistical analysis
- **Entry Point:** `salary_analyzer()`

#### B. Code Structure Analysis

**Python Files (13):**
1. `__init__.py` (45 LOC) - Package initialization
2. `employee_db.py` (85 LOC) - Employee database with sample data
3. `salary_analyzer_class.py` (50 LOC) - Main analyzer class
4. `data_validator.py` (23 LOC) - Data validation utilities
5. `csv_processor.py` (35 LOC) - CSV data processing
6. `json_processor.py` (33 LOC) - JSON data processing
7. `data_scaler.py` (42 LOC) - Data normalization/scaling
8. `feature_engineer.py` (40 LOC) - Feature engineering for ML
9. `model_evaluator.py` (49 LOC) - ML model evaluation
10. `url_validator.py` (33 LOC) - URL validation utilities
11. `content_extractor.py` (41 LOC) - Web content extraction
12. `crawl_manager.py` (66 LOC) - Web crawler management
13. `robots_txt_parser.py` (61 LOC) - robots.txt parser

**Total Lines of Code:** 603

**Classes (12):**
- **Data Processing:** `DataValidator`, `CSVProcessor`, `JSONProcessor`
- **Database:** `EmployeeDB`, `SalaryAnalyzer`
- **ML Utilities:** `DataScaler`, `FeatureEngineer`, `ModelEvaluator`
- **Web Crawler:** `URLValidator`, `ContentExtractor`, `CrawlManager`, `RobotsTxtParser`

**Key Methods (59 total):**
- `EmployeeDB.get_all_employees()` - Retrieve employee data
- `EmployeeDB.get_employee_by_id()` - Get specific employee
- `EmployeeDB.get_employees_by_department()` - Department filtering
- `SalaryAnalyzer.calculate_average()` - Average salary calculation
- `DataValidator.validate()` - Data validation
- `CSVProcessor.read_csv()` - CSV reading
- `JSONProcessor.parse_json()` - JSON parsing
- `DataScaler.normalize()` - Data normalization
- `FeatureEngineer.create_features()` - Feature engineering

#### C. Data Files
**None** - Uses hardcoded `EMPLOYEE_DATA` dictionary with 15 employees

**Employee Data Structure:**
```python
{
    'E001': {'name': 'Alice Johnson', 'department': 'Engineering',
             'salary': 95000, 'years_of_experience': 5},
    # ... 14 more employees
}
```

#### D. Module Architecture

**Import Dependencies:**
```python
# Organized into 4 modules:
# 1. Data Processing Module
# 2. Employee Database Module
# 3. ML Utilities Module
# 4. Web Crawler Module
```

**Package Exports:**
```python
__all__ = [
    'DataValidator', 'CSVProcessor', 'JSONProcessor',
    'EmployeeDB', 'EMPLOYEE_DATA', 'SalaryAnalyzer',
    'DataScaler', 'FeatureEngineer', 'ModelEvaluator',
    'URLValidator', 'ContentExtractor', 'CrawlManager', 'RobotsTxtParser'
]
```

#### E. Complexity Metrics
- **Classes:** 12
- **Methods:** 59
- **Cyclomatic Complexity:** Low-Medium (data processing)
- **Integration Complexity:** Medium (4 logical modules)
- **Domain Complexity:** Low (straightforward statistical analysis)

**Expected Result:** Average salary between $30,000 - $200,000

---

### 2.4 Inventory Replenishment

**Location:** `/dataset/inventory_replenishment/`

#### A. Basic Information
- **Dataset ID:** 4
- **Domain:** E-commerce / Retail
- **Purpose:** Identify products with low stock levels requiring replenishment
- **Task Type:** Inventory management and alerting
- **Entry Point:** `inventory_low_stock_alert()`

#### B. Code Structure Analysis

**Python Files (8):**
1. `__init__.py` (20 LOC) - Package initialization
2. `product.py` (27 LOC) - Product model
3. `stock_level.py` (35 LOC) - Stock tracking
4. `sales_transaction.py` (26 LOC) - Sales records
5. `purchase_order.py` (28 LOC) - Purchase orders
6. `warehouse.py` (177 LOC) - Warehouse system with sample data
7. `demand_forecaster.py` (128 LOC) - Demand forecasting
8. `order_optimizer.py` (128 LOC) - Order optimization

**Total Lines of Code:** 569

**Classes (7):**
- **Core Models:** `Product`, `StockLevel`, `SalesTransaction`, `PurchaseOrder`, `Warehouse`
- **Analytics:** `DemandForecaster`, `OrderOptimizer`

**Key Methods (34 total):**
- `Warehouse.get_all_products()` - Get product list
- `Warehouse.get_current_stock()` - Get stock level for SKU
- `Warehouse.add_stock()` - Add inventory
- `Warehouse.remove_stock()` - Remove inventory
- `Product.__init__()` - Product with reorder_point
- `DemandForecaster.forecast_demand()` - Predict future demand
- `OrderOptimizer.optimize_order()` - Optimize purchase orders
- `create_sample_warehouse()` - Generate test data

#### C. Data Files
**None** - Uses programmatically generated warehouse with 6 products

**Sample Products:**
- SKU001: Laptop (current: 8, reorder: 10) - LOW STOCK
- SKU002: Desk Chair (current: 15, reorder: 20) - LOW STOCK
- SKU003: Monitor (current: 50, reorder: 30) - OK
- SKU004: Keyboard (current: 18, reorder: 25) - LOW STOCK
- SKU005: Mouse (current: 35, reorder: 40) - LOW STOCK
- SKU006: Webcam (current: 10, reorder: 15) - LOW STOCK

#### D. Module Architecture

**Import Dependencies:**
```python
stock_level.py → product.py
sales_transaction.py → product.py
purchase_order.py → product.py
warehouse.py → all core models
analytics → warehouse, core models
```

**Package Exports:**
```python
__all__ = [
    'Product', 'StockLevel', 'SalesTransaction', 'PurchaseOrder', 'Warehouse',
    'DemandForecaster', 'OrderOptimizer', 'create_sample_warehouse'
]
```

#### E. Complexity Metrics
- **Classes:** 7
- **Methods:** 34
- **Cyclomatic Complexity:** Medium (inventory logic)
- **Integration Complexity:** Medium (7 related classes)
- **Domain Complexity:** Medium (inventory management rules)

**Expected Result:** List of 5 dicts with keys: `sku`, `name`, `current_stock`, `reorder_point`, `deficit`

---

### 2.5 Book Recommender

**Location:** `/dataset/book_recommender/`

#### A. Basic Information
- **Dataset ID:** 9
- **Domain:** Media Recommendation
- **Purpose:** Filter books by genre with progressive API evolution (v1, v2, v3)
- **Task Type:** Data filtering with API versioning
- **Entry Point:** `book_recommender(genre)`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (minimal stub)

**Total Lines of Code:** ~5

**Classes:** 0

#### C. Data Files Analysis

**File:** `books.csv` (101 lines including header)

**Schema:**
- `isbn` (string) - ISBN-13 identifier
- `title` (string) - Book title
- `author` (string) - Author name
- `genre` (string) - Book genre category
- `year` (integer) - Publication year
- `rating` (float) - Rating 0.0-5.0

**Sample Data:**
```csv
isbn,title,author,genre,year,rating
978-6714714797,Book Title 1,Gabriel Garcia Marquez,Non-Fiction,2019,3.1
978-2300828189,Book Title 2,Agatha Christie,Thriller,2013,3.5
```

**Statistics:**
- **Total Books:** 100
- **Authors:** 15+ (Agatha Christie, Dan Brown, Stephen King, Jane Austen, Haruki Murakami, etc.)
- **Genres:** 12 (Fiction, Non-Fiction, Thriller, Mystery, Fantasy, Science Fiction, Romance, Biography, History, Self-Help)
- **Rating Range:** 3.0 - 5.0
- **Year Range:** 1990 - 2024

#### D. Module Architecture

**API Versioning:**
- **v1:** Returns `list[str]` of titles
- **v2:** Returns `dict` with `titles`, `count`, `avg_rating`
- **v3:** Returns `dict` with JSON-LD structure (`@context`, `@type`, `numberOfItems`)

**Version Detection:** `os.environ.get('API_VERSION', 'v1')`

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 1 function to implement
- **Data Complexity:** Low (simple CSV)
- **Integration Complexity:** Low (standalone)
- **Domain Complexity:** Low (genre filtering)

---

### 2.6 Friend Suggester

**Location:** `/dataset/friend_suggester/`

#### A. Basic Information
- **Dataset ID:** 11
- **Domain:** Social Network
- **Purpose:** Recommend friends based on mutual connections, interests, and activity
- **Task Type:** Graph analysis with progressive enhancement
- **Entry Point:** `friend_suggestions(user_id)`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (minimal stub)

**Total Lines of Code:** ~5

**Classes:** 0

#### C. Data Files Analysis

**File:** `social_graph.json` (2,899 lines)

**Schema:**
```json
{
  "users": [
    {
      "user_id": "U001",
      "username": "user1",
      "friends": ["U052", "U074", ...],
      "interests": ["Travel", "Reading", "Fashion"],
      "activity": {
        "level": "medium",
        "posts_per_week": 6,
        "likes_per_week": 91,
        "comments_per_week": 12
      },
      "member_since": "2019-12-14"
    }
  ],
  "total_users": 100
}
```

**Statistics:**
- **Total Users:** 100 (U001 - U100)
- **Average Friends per User:** ~9
- **Interests:** 11 categories (Travel, Reading, Fashion, Technology, Sports, Gaming, Art, Fitness, Cooking, Photography, Music, Hiking, Gardening, Movies)
- **Activity Levels:** low, medium, high, very_high
- **Network Density:** Medium (highly connected)

**Graph Properties:**
- **Nodes:** 100 users
- **Edges:** ~450 friendships (bidirectional)
- **Average Degree:** 9
- **Interest Overlap:** Moderate

#### D. Module Architecture

**Recommendation Modes:**
- **basic:** Score = mutual_friends_count
- **enhanced:** Score = (mutual_friends * 2.0) + (common_interests * 1.5)
- **advanced:** Enhanced + 1.0 bonus if activity levels match

**Mode Detection:** `os.environ.get('RECOMMENDATION_MODE', 'basic')`

**Output:** Top 5 suggestions sorted by score descending

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 1 function to implement
- **Data Complexity:** Medium (graph structure)
- **Integration Complexity:** Low (standalone)
- **Domain Complexity:** Medium (graph algorithms, scoring)

---

### 2.7 MovieLens Dataset

**Location:** `/dataset/movielens_dataset/`

#### A. Basic Information
- **Dataset ID:** 8
- **Domain:** Media Recommendation
- **Purpose:** API interface evolution - auto-detect caller context and switch return formats
- **Task Type:** Advanced API design with introspection
- **Entry Point:** `movie_api()`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (minimal stub)

**Total Lines of Code:** ~5

**Classes:** 0

#### C. Data Files Analysis

**File:** `movie.csv` (101 lines including header)

**Schema:**
- `movieId` (integer) - Movie identifier
- `title` (string) - Movie title with year
- `genres` (string) - Pipe-separated genre list

**Sample Data:**
```csv
"movieId","title","genres"
1,"Toy Story (1995)","Adventure|Animation|Children|Comedy|Fantasy"
2,"Jumanji (1995)","Adventure|Children|Fantasy"
```

**Statistics:**
- **Total Movies:** 100
- **Year Range:** 1995-1996 (classic MovieLens dataset subset)
- **Genres:** 18+ (Action, Adventure, Animation, Children, Comedy, Crime, Drama, Fantasy, Horror, Mystery, Romance, Sci-Fi, Thriller, IMAX, Documentary, War, etc.)
- **Multi-Genre:** Most movies have 2-3 genres

**Notable Films:**
- Toy Story (1995)
- Jumanji (1995)
- The Usual Suspects (1995)
- Seven (Se7en) (1995)
- Twelve Monkeys (1995)

#### D. Module Architecture

**Auto-Detection via Call Stack Introspection:**
- **v1:** Returns `list[str]` of 100 titles
- **v2:** Returns `dict` with metadata
- **v3:** Returns JSON-LD structured data

**Detection Method:** Inspect call stack to determine caller context

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 1 function to implement
- **Data Complexity:** Low (simple CSV)
- **Integration Complexity:** Medium (requires introspection)
- **Domain Complexity:** Medium (call stack analysis)

---

### 2.8 Performance Tracker

**Location:** `/dataset/performance_tracker/`

#### A. Basic Information
- **Dataset ID:** 10
- **Domain:** HR Analytics
- **Purpose:** Generate employee performance reports with multiple modes
- **Task Type:** Data aggregation and reporting
- **Entry Point:** `performance_report(employee_id, report_type)`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (minimal stub)

**Total Lines of Code:** ~5

**Classes:** 0

#### C. Data Files Analysis

**File:** `performance_reviews.csv` (51 lines including header)

**Schema:**
- `employee_id` (string) - Employee identifier (E001-E050)
- `employee_name` (string) - Employee name
- `department` (string) - Department name
- `position` (string) - Job position
- `review_period` (string) - Quarter (Q1-Q4 2024)
- `technical_score` (integer) - Technical skills 0-5
- `communication_score` (integer) - Communication 0-5
- `teamwork_score` (integer) - Teamwork 0-5
- `leadership_score` (integer) - Leadership 0-5
- `overall_rating` (float) - Overall rating
- `goals_status` (string) - Met/Exceeded/Not Met/Partially Met
- `feedback` (string) - Performance feedback text

**Statistics:**
- **Total Employees:** 50 (E001-E050)
- **Departments:** 8 (Operations, Customer Support, Engineering, Finance, Sales, Marketing, HR)
- **Positions:** 5 (Junior, Mid-level, Senior, Lead, Manager)
- **Review Periods:** Q1-Q4 2024
- **Score Range:** 0-5 for individual skills
- **Overall Rating Range:** 2.0-4.8

**Department Distribution:**
- Operations: 8 employees
- Customer Support: 7 employees
- Finance: 11 employees
- Sales: 7 employees
- Engineering: 6 employees
- Marketing: 2 employees
- HR: 2 employees

#### D. Module Architecture

**Report Types:**
- **summary:** Returns single dict with `employee_id`, `overall_rating`, `goals_status`
- **detailed:** Returns single dict with ALL CSV columns
- **department:** When `employee_id=None`, groups by department with `avg_rating` and `count`

**Parameters:**
- `employee_id` (optional string) - Target employee or None for department mode
- `report_type` (string, default='summary') - Report format

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 1 function to implement
- **Data Complexity:** Medium (multi-field CSV)
- **Integration Complexity:** Low (standalone)
- **Domain Complexity:** Low (data aggregation)

---

### 2.9 IoT Sensor Pipeline

**Location:** `/dataset/iot_sensor_pipeline/`

#### A. Basic Information
- **Dataset ID:** 7
- **Domain:** IoT Data Processing
- **Purpose:** Cross-session problem - parse sensor data then aggregate temperature
- **Task Type:** Multi-session composition
- **Entry Point:** Session 1: `parse_sensor_reading()`, Session 2: `aggregate_temperature()`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (5 LOC) - Minimal stub for cross-session work

**Total Lines of Code:** 5

**Classes:** 0

#### C. Data Files
**None** - Uses string-based sensor data format

**Sensor Data Format:**
```
"T:25.5|H:60|TS:1234567890"
```

**Fields:**
- T: Temperature (float)
- H: Humidity (float)
- TS: Timestamp (integer, Unix epoch)

#### D. Module Architecture

**Session 1:**
- Implement `parse_sensor_reading(raw_string)` → `dict`
- Split by `|`, then by `:`
- Convert types: T→float, H→float, TS→int
- Handle conversion errors → set to None

**Session 2 (depends on Session 1):**
- Implement `aggregate_temperature(readings_list)` → `float`
- Use `parse_sensor_reading()` from Session 1
- Calculate average of valid temperatures
- Round to 2 decimals
- Return 0.0 if no valid temperatures

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 2 functions to implement across sessions
- **Data Complexity:** Low (simple string parsing)
- **Integration Complexity:** High (cross-session dependency)
- **Domain Complexity:** Low (basic data processing)

**Cross-Session Requirement:** Session 2 must load and use code from Session 1

---

### 2.10 Matrix Eigenvalue Composition

**Location:** `/dataset/matrix_eigenvalue_composition/`

#### A. Basic Information
- **Dataset ID:** 5
- **Domain:** Linear Algebra / Mathematics
- **Purpose:** Cross-session problem - basic matrix ops then eigenvalue calculations
- **Task Type:** Multi-session composition with global state
- **Entry Point:** Session 1: `matrix_operations()`, Session 2: `advanced_matrix_ops()`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (5 LOC) - Minimal stub for cross-session work

**Total Lines of Code:** 5

**Classes:** 0

#### C. Data Files
**None** - Works with numerical arrays

**Input Format:**
```python
matrix = [[1, 2], [3, 4]]  # 2x2 matrix as nested list
```

#### D. Module Architecture

**Session 1:**
- Implement `matrix_operations(matrix)`
- Perform basic matrix multiplication
- Store results in `computation_cache` (global variable)

**Session 2 (depends on Session 1):**
- Implement `advanced_matrix_ops(matrix)`
- Use `matrix_operations()` from Session 1
- Access `computation_cache` global variable
- Perform eigenvalue calculations using NumPy

**Global State:**
```python
computation_cache = {}  # Shared between sessions
```

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 2 functions to implement across sessions
- **Data Complexity:** Medium (matrix operations)
- **Integration Complexity:** High (cross-session + global state)
- **Domain Complexity:** Medium (linear algebra)

**Dependencies:** NumPy for eigenvalue computation

**Cross-Session Requirements:**
1. Load previous session code
2. Access global variables
3. Reuse existing functions

---

### 2.11 Portfolio Risk Calculator

**Location:** `/dataset/portfolio_risk_calculator/`

#### A. Basic Information
- **Dataset ID:** 6
- **Domain:** Financial Analysis
- **Purpose:** Cross-session problem - calculate stock volatility then portfolio risk
- **Task Type:** Multi-session composition
- **Entry Point:** Session 1: `calculate_stock_volatility()`, Session 2: `portfolio_risk_assessment()`

#### B. Code Structure Analysis

**Python Files (1):**
1. `__init__.py` (5 LOC) - Minimal stub for cross-session work

**Total Lines of Code:** 5

**Classes:** 0

#### C. Data Files
**None** - Works with numerical price data

**Input Formats:**

**Session 1:**
```python
prices = [100.0, 102.0, 98.0, 101.0, 99.0]  # Daily stock prices
```

**Session 2:**
```python
portfolio = {
    'AAPL': {'prices': [150.0, 152.0, 148.0, 155.0], 'allocation': 0.6},
    'GOOGL': {'prices': [2800.0, 2820.0, 2790.0, 2850.0], 'allocation': 0.4}
}
```

#### D. Module Architecture

**Session 1:**
- Implement `calculate_stock_volatility(prices)` → `float`
- Calculate daily returns: `(price[i] - price[i-1]) / price[i-1]`
- Calculate mean of returns
- Calculate variance: `avg((return - mean)²)`
- Return `sqrt(variance) * 100` as percentage
- Return 0.0 if fewer than 2 prices

**Session 2 (depends on Session 1):**
- Implement `portfolio_risk_assessment(portfolio_dict)` → `float`
- For each stock:
  - Call `calculate_stock_volatility(stock['prices'])`
  - Multiply by `stock['allocation']`
- Sum all weighted volatilities
- Return total portfolio risk

**Risk Formula:**
```
portfolio_risk = Σ(volatility_i * allocation_i)
```

#### E. Complexity Metrics
- **Classes:** 0
- **Methods:** 2 functions to implement across sessions
- **Data Complexity:** Medium (financial calculations)
- **Integration Complexity:** High (cross-session dependency)
- **Domain Complexity:** Medium (financial mathematics)

**Cross-Session Requirement:** Session 2 must load and use `calculate_stock_volatility()` from Session 1

---

## 3. Comparative Analysis

### 3.1 Code-Heavy vs Data-Only Datasets

| Category | Datasets | Total Python Files | Total Classes | Total LOC | Avg LOC/File |
|----------|----------|-------------------|---------------|-----------|--------------|
| **Code-Heavy** | 4 | 43 | 49 | 2,685 | 62.4 |
| **Data-Only** | 4 | 4 (stubs) | 0 | ~20 | 5 |
| **Minimal** | 3 | 3 (stubs) | 0 | 15 | 5 |

### 3.2 Lines of Code Distribution

**Code-Heavy Datasets:**

| Dataset | Python LOC | Percentage |
|---------|-----------|------------|
| student_gpa_calculator | 773 | 28.8% |
| patient_risk_analyzer | 740 | 27.6% |
| salary_analyzer | 603 | 22.5% |
| inventory_replenishment | 569 | 21.2% |

**Visualization:**
```
student_gpa_calculator    ████████████████████████████ 773 LOC
patient_risk_analyzer     ███████████████████████████ 740 LOC
salary_analyzer          ████████████████████████ 603 LOC
inventory_replenishment  ██████████████████████ 569 LOC
```

### 3.3 Class Count Distribution

| Dataset | Classes | Methods | Methods/Class Ratio |
|---------|---------|---------|-------------------|
| patient_risk_analyzer | 20 | 59 | 2.95 |
| salary_analyzer | 12 | 59 | 4.92 |
| student_gpa_calculator | 10 | 43 | 4.30 |
| inventory_replenishment | 7 | 34 | 4.86 |

### 3.4 Domain Coverage

| Domain | Datasets | Complexity Level |
|--------|----------|-----------------|
| Healthcare | 1 | High |
| Education | 1 | Medium |
| HR Analytics | 2 | Low-Medium |
| E-commerce/Retail | 1 | Medium |
| Media Recommendation | 2 | Low-Medium |
| Social Networks | 1 | Medium |
| IoT | 1 | Low |
| Mathematics | 1 | Medium |
| Finance | 1 | Medium |

### 3.5 Data File Statistics

| Dataset | File Type | Lines | Records | Data Complexity |
|---------|-----------|-------|---------|----------------|
| book_recommender | CSV | 101 | 100 | Low |
| friend_suggester | JSON | 2,899 | 100 users | Medium-High |
| movielens_dataset | CSV | 101 | 100 | Low |
| performance_tracker | CSV | 51 | 50 | Low |

**Total Data Lines:** 3,152

### 3.6 Problem Type Classification

| Type | Count | Datasets |
|------|-------|----------|
| **Single Function Implementation** | 4 | patient_risk_analyzer, student_gpa_calculator, salary_analyzer, inventory_replenishment |
| **API Evolution/Versioning** | 2 | book_recommender, movielens_dataset |
| **Recommendation System** | 2 | book_recommender, friend_suggester |
| **Reporting/Aggregation** | 1 | performance_tracker |
| **Cross-Session Composition** | 3 | iot_sensor_pipeline, matrix_eigenvalue_composition, portfolio_risk_calculator |

### 3.7 Complexity Spectrum

**Low Complexity (3):**
- book_recommender - Simple CSV filtering
- performance_tracker - Basic data aggregation
- iot_sensor_pipeline - String parsing

**Medium Complexity (5):**
- salary_analyzer - Data processing utilities
- inventory_replenishment - Inventory management
- student_gpa_calculator - GPA calculations
- movielens_dataset - Call stack introspection
- friend_suggester - Graph analysis
- portfolio_risk_calculator - Financial math

**High Complexity (3):**
- patient_risk_analyzer - 20 interconnected classes
- matrix_eigenvalue_composition - Linear algebra + cross-session
- Multi-session datasets - Session continuity requirements

### 3.8 Token Usage Estimates

**Conservative Token Estimates:**

| Dataset | Code Tokens | Data Tokens | Total Tokens |
|---------|-------------|-------------|--------------|
| patient_risk_analyzer | ~3,000 | 0 | ~3,000 |
| student_gpa_calculator | ~3,100 | 0 | ~3,100 |
| salary_analyzer | ~2,400 | 0 | ~2,400 |
| inventory_replenishment | ~2,300 | 0 | ~2,300 |
| book_recommender | ~20 | ~600 | ~620 |
| friend_suggester | ~20 | ~17,000 | ~17,020 |
| movielens_dataset | ~20 | ~600 | ~620 |
| performance_tracker | ~20 | ~1,000 | ~1,020 |
| iot_sensor_pipeline | ~20 | 0 | ~20 |
| matrix_eigenvalue_composition | ~20 | 0 | ~20 |
| portfolio_risk_calculator | ~20 | 0 | ~20 |

**Total Estimated Tokens:** ~32,140

**Notes:**
- Code tokens: ~4 tokens per line of code
- Data tokens: ~6 tokens per line of JSON, ~4 tokens per line of CSV
- friend_suggester has highest token count due to large JSON

---

## 4. Technical Specifications

### 4.1 Python Version Compatibility

**All datasets are compatible with Python 3.7+**

**Type Hints:** Extensive use of type hints in code-heavy datasets
- `from typing import List, Dict, Optional, Tuple, Union`
- Enum types in student_gpa_calculator

**Modern Features:**
- f-strings for string formatting
- Dataclass-like patterns (manual __init__)
- List comprehensions
- Dictionary comprehensions

### 4.2 Dependencies

**Core Python Standard Library:**
- `datetime` - Date/time handling (patient_risk_analyzer, conditions, medical records)
- `typing` - Type annotations
- `enum` - Enumerations (ScholarshipType)
- `os` - Environment variables (API versioning)
- `inspect` - Call stack introspection (movielens_dataset)
- `csv` - CSV processing (data-only datasets)
- `json` - JSON processing (friend_suggester)

**External Dependencies (Minimal Dataset Requirements):**
- `numpy` - Matrix operations and eigenvalue calculations (matrix_eigenvalue_composition)

**No other external dependencies required for basic functionality**

### 4.3 Import Structure

**Code-Heavy Datasets Pattern:**
```python
# __init__.py structure
"""Package documentation"""

# Core models
from .model1 import *
from .model2 import *

# Helper utilities
from .helper1 import *
from .helper2 import *

# Explicit exports
__all__ = [
    'Class1', 'Class2', 'function1',
    # ... comprehensive list
]
```

**Common Import Pattern:**
```python
# In module files
from typing import List, Dict, Optional
from datetime import datetime
from .dependency import DependencyClass
```

### 4.4 Package Organization

**All datasets follow Python package structure:**
```
dataset_name/
├── __init__.py          # Package initialization, exports
├── core_model1.py       # Core data models
├── core_model2.py
├── helper1.py           # Helper/utility classes
├── helper2.py
├── data.csv             # Data files (if applicable)
└── problem.json         # Problem definition
```

**Key Files:**
- `__init__.py` - Package initialization, imports, __all__ exports
- `problem.json` - Problem definition, test cases, domain info
- Core model files - Essential business logic classes
- Helper files - Utility classes and functions

### 4.5 Naming Conventions

**File Names:**
- Snake_case for all Python files
- Descriptive names: `patient_risk_analyzer.py`, `grade_calculator.py`

**Class Names:**
- PascalCase: `Patient`, `University`, `EmployeeDB`
- Descriptive: `DrugInteractionChecker`, `ScholarshipEvaluator`

**Function/Method Names:**
- Snake_case: `get_patient()`, `calculate_gpa()`
- Verb-noun pattern: `add_condition()`, `has_abnormal_vitals()`

**Constants:**
- UPPER_SNAKE_CASE: `EMPLOYEE_DATA`

### 4.6 Code Quality Patterns

**Docstrings:**
```python
"""
Module/Class docstring
Brief description of purpose
"""
```

**Type Annotations:**
```python
def get_patient(self, patient_id: str) -> Optional[Patient]:
    """Retrieve patient by ID"""
    return self.patients.get(patient_id)
```

**Error Handling:**
- Minimal explicit error handling (designed for testing)
- Type checking via type hints
- Validation in helper classes (DataValidator, URLValidator)

**Data Generation Functions:**
- `create_sample_hospital()` - Patient risk analyzer
- `create_sample_university()` - Student GPA calculator
- `create_sample_warehouse()` - Inventory replenishment
- Consistent pattern across datasets

### 4.7 Testing Infrastructure

**Test Data Embedded in problem.json:**
```json
{
  "id": 1,
  "entry_point": "function_name",
  "test_code": "\n# Executable test code\nassert ...\n"
}
```

**Test Characteristics:**
- Executable Python code as string
- Multiple test cases per problem
- Assertion-based validation
- Expected value testing
- Edge case coverage

---

## 5. Appendix: Summary Tables

### 5.1 Complete Dataset Summary

| # | Dataset Name | Domain | Type | Python Files | Classes | LOC | Data Files | Complexity |
|---|--------------|--------|------|--------------|---------|-----|------------|------------|
| 1 | patient_risk_analyzer | Healthcare | Code-Heavy | 12 | 20 | 740 | 0 | High |
| 2 | student_gpa_calculator | Education | Code-Heavy | 10 | 10 | 773 | 0 | Medium |
| 3 | salary_analyzer | HR Analytics | Code-Heavy | 13 | 12 | 603 | 0 | Medium |
| 4 | inventory_replenishment | E-commerce | Code-Heavy | 8 | 7 | 569 | 0 | Medium |
| 5 | book_recommender | Media | Data-Only | 1 | 0 | 5 | 1 CSV (100) | Low |
| 6 | friend_suggester | Social Network | Data-Only | 1 | 0 | 5 | 1 JSON (100) | Medium |
| 7 | movielens_dataset | Media | Data-Only | 1 | 0 | 5 | 1 CSV (100) | Medium |
| 8 | performance_tracker | HR Analytics | Data-Only | 1 | 0 | 5 | 1 CSV (50) | Low |
| 9 | iot_sensor_pipeline | IoT | Minimal | 1 | 0 | 5 | 0 | Low |
| 10 | matrix_eigenvalue_composition | Mathematics | Minimal | 1 | 0 | 5 | 0 | Medium |
| 11 | portfolio_risk_calculator | Finance | Minimal | 1 | 0 | 5 | 0 | Medium |
| **TOTAL** | **11** | **9 domains** | **3 types** | **48** | **49** | **2,685** | **4** | **Mixed** |

### 5.2 File Distribution

| File Type | Count | Purpose |
|-----------|-------|---------|
| `__init__.py` | 11 | Package initialization and exports |
| Core model files (`.py`) | 15 | Essential business logic classes |
| Helper utility files (`.py`) | 22 | Supporting classes and functions |
| `problem.json` | 11 | Problem definitions and test cases |
| Data files (`.csv`, `.json`) | 4 | Sample datasets |
| **Total Files** | **63** | |

### 5.3 Class Distribution by Dataset

**Detailed Class Counts:**

| Dataset | Core Classes | Helper Classes | Total |
|---------|--------------|----------------|-------|
| patient_risk_analyzer | 4 | 16 | 20 |
| salary_analyzer | 2 | 10 | 12 |
| student_gpa_calculator | 5 | 5 | 10 |
| inventory_replenishment | 5 | 2 | 7 |
| **Others** | 0 | 0 | 0 |

### 5.4 Method Distribution

| Dataset | Total Methods | Avg Methods/Class |
|---------|---------------|------------------|
| patient_risk_analyzer | 59 | 2.95 |
| salary_analyzer | 59 | 4.92 |
| student_gpa_calculator | 43 | 4.30 |
| inventory_replenishment | 34 | 4.86 |

### 5.5 Domain Distribution

**Coverage Across Application Domains:**

```
Healthcare             ██████████ 1 dataset  (patient_risk_analyzer)
Education              ██████████ 1 dataset  (student_gpa_calculator)
HR Analytics           ████████████████████ 2 datasets (salary_analyzer, performance_tracker)
E-commerce/Retail      ██████████ 1 dataset  (inventory_replenishment)
Media Recommendation   ████████████████████ 2 datasets (book_recommender, movielens_dataset)
Social Networks        ██████████ 1 dataset  (friend_suggester)
IoT                    ██████████ 1 dataset  (iot_sensor_pipeline)
Mathematics            ██████████ 1 dataset  (matrix_eigenvalue_composition)
Finance                ██████████ 1 dataset  (portfolio_risk_calculator)
```

### 5.6 Problem Type Distribution

| Problem Type | Count | Description |
|--------------|-------|-------------|
| Single Function Implementation | 4 | Implement one function using provided classes |
| API Evolution | 2 | Progressive API versioning (v1, v2, v3) |
| Recommendation System | 2 | Filter/recommend based on criteria |
| Data Aggregation | 1 | Multi-mode reporting |
| Cross-Session Composition | 3 | Multi-session with dependencies |

### 5.7 Test Coverage

| Dataset | Test Cases | Test Types |
|---------|-----------|------------|
| patient_risk_analyzer | 3 | High/Medium/Low risk patients |
| student_gpa_calculator | 3 | Good/Average/Struggling students |
| salary_analyzer | 1 | Average calculation validation |
| inventory_replenishment | 5 | Low stock verification |
| book_recommender | 3 | v1/v2/v3 API versions |
| friend_suggester | 3 | basic/enhanced/advanced modes |
| movielens_dataset | 3 | Auto-detection formats |
| performance_tracker | 3 | summary/detailed/department modes |
| iot_sensor_pipeline | 2 | Parse + Aggregate |
| matrix_eigenvalue_composition | 1 | Cross-session composition |
| portfolio_risk_calculator | 2 | Volatility + Portfolio |

---

## Conclusion

This comprehensive analysis documents 11 datasets comprising **2,685 lines of Python code** across **49 classes** and **195+ methods**, plus **3,152 lines of data** in CSV/JSON formats. The datasets cover **9 distinct application domains** with varying complexity levels from simple data filtering to complex multi-class systems with cross-session dependencies.

### Key Insights:

1. **Balanced Complexity:** Mix of simple (data-only), medium (single implementation), and complex (multi-class, cross-session) problems
2. **Domain Diversity:** Comprehensive coverage across healthcare, education, finance, e-commerce, media, social networks, IoT, and mathematics
3. **Modern Python:** Extensive type hints, clean architecture, well-organized packages
4. **Self-Contained:** Minimal external dependencies (only NumPy for one dataset)
5. **Progressive Challenge:** From ~20 LOC stubs to 773 LOC multi-class systems

### Use Cases:

- **AI Agent Testing:** Self-evolution and code generation capabilities
- **Code Understanding:** Context learning and comprehension
- **API Design:** Version evolution and backward compatibility
- **Cross-Session Memory:** Persistent state and code reuse
- **Domain Adaptation:** Multi-domain knowledge application

---

**Document Version:** 1.0
**Last Updated:** 2025-10-12
**Total Datasets Analyzed:** 11/11 (100%)
**Analysis Completeness:** Comprehensive
