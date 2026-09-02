# Official Competencies, Baseline Questions, and Resources Data for India's Statistical System

COMPETENCIES_SEED = [
    {
        "code": "STAT_SURVEY",
        "name": "Survey Methodology & Sampling Design",
        "domain": "Survey Operations",
        "description": "Techniques of probability sampling, stratified multistage sampling design, sampling frames, weighting procedures, and non-sampling error minimization in large-scale national socioeconomic surveys.",
        "required_level": 80.0,
        "weight": 1.2
    },
    {
        "code": "STAT_NAT_ACC",
        "name": "National Accounts Statistics & Macro Aggregates",
        "domain": "Macroeconomic Statistics",
        "description": "System of National Accounts (SNA 2008), Gross Domestic Product (GDP), Gross Value Added (GVA), Supply and Use Tables (SUT), institutional sector accounts, and capital formation estimation.",
        "required_level": 85.0,
        "weight": 1.3
    },
    {
        "code": "STAT_COMPUTE",
        "name": "Statistical Computing & Data Science",
        "domain": "Computing & Informatics",
        "description": "Statistical programming using Python, R, STATA, and SQL for data transformation, unit-level microdata processing, econometric modeling, automated report pipelines, and reproducible research.",
        "required_level": 80.0,
        "weight": 1.2
    },
    {
        "code": "STAT_PRICE_IND",
        "name": "Price Statistics & Index Numbers",
        "domain": "Price & Industrial Statistics",
        "description": "Compilation methodology of Consumer Price Index (CPI), Index of Industrial Production (IIP), Wholesale Price Index (WPI), Laspeyres/Paasche index formulations, and basket revision protocols.",
        "required_level": 75.0,
        "weight": 1.0
    },
    {
        "code": "STAT_LABOUR",
        "name": "Labour & Demographic Statistics",
        "domain": "Socioeconomic Statistics",
        "description": "Periodic Labour Force Survey (PLFS) concepts, Usual Principal & Subsidiary Status (UPSS), Current Weekly Status (CWS), Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), and unemployment metrics.",
        "required_level": 80.0,
        "weight": 1.1
    },
    {
        "code": "STAT_DATA_GOV",
        "name": "Data Management & eSankhyiki Governance",
        "domain": "Data Governance",
        "description": "MoSPI National Metadata Standards, eSankhyiki portal data architecture, microdata anonymization, FAIR data principles, API-based dissemination, and open government data security.",
        "required_level": 75.0,
        "weight": 1.0
    },
    {
        "code": "STAT_QUALITY",
        "name": "Statistical Quality Assurance & Audit",
        "domain": "Quality & Standards",
        "description": "United Nations Fundamental Principles of Official Statistics, National Quality Assurance Frameworks (NQAF), data consistency auditing, imputation methods, and field survey supervision protocols.",
        "required_level": 80.0,
        "weight": 1.1
    },
    {
        "code": "STAT_VIZ_COMM",
        "name": "Data Visualization & Official Communication",
        "domain": "Dissemination",
        "description": "Visual storytelling for policy makers, interactive dashboard development, Sustainable Development Goal (SDG) National Indicator reporting, statistical press release drafting, and public data literacy.",
        "required_level": 70.0,
        "weight": 0.9
    },
    {
        "code": "STAT_IND_AGRI",
        "name": "Industrial & Enterprise Statistics",
        "domain": "Enterprise Statistics",
        "description": "Annual Survey of Industries (ASI) factory frame, NIC/NPC classifications, invested capital estimation, Gross Output, Net Value Added calculation in organized manufacturing, and service sector enterprise surveys.",
        "required_level": 75.0,
        "weight": 1.0
    }
]

DIVISION_PROFILES = {
    "MoSPI National Accounts Division (NAD)": {
        "division_code": "NAD",
        "description": "Compilation of GDP, GVA, Supply and Use Tables, and capital formation accounts under SNA 2008 framework.",
        "core_competencies": ["STAT_NAT_ACC", "STAT_COMPUTE", "STAT_PRICE_IND", "STAT_QUALITY", "STAT_DATA_GOV"],
        "benchmarks": {
            "STAT_NAT_ACC": 90.0,
            "STAT_COMPUTE": 85.0,
            "STAT_PRICE_IND": 80.0,
            "STAT_QUALITY": 80.0,
            "STAT_DATA_GOV": 75.0,
            "STAT_SURVEY": 70.0,
            "STAT_LABOUR": 70.0,
            "STAT_VIZ_COMM": 75.0,
            "STAT_IND_AGRI": 75.0
        },
        "weights": {
            "STAT_NAT_ACC": 1.5,
            "STAT_COMPUTE": 1.3,
            "STAT_PRICE_IND": 1.2,
            "STAT_QUALITY": 1.1,
            "STAT_DATA_GOV": 1.0,
            "STAT_SURVEY": 0.9,
            "STAT_LABOUR": 0.9,
            "STAT_VIZ_COMM": 1.0,
            "STAT_IND_AGRI": 1.0
        }
    },
    "MoSPI Field Operations Division (FOD)": {
        "division_code": "FOD",
        "description": "Execution of nationwide socioeconomic sample surveys (PLFS, HCES), ASI field visits, and data collection.",
        "core_competencies": ["STAT_SURVEY", "STAT_LABOUR", "STAT_QUALITY", "STAT_IND_AGRI", "STAT_DATA_GOV"],
        "benchmarks": {
            "STAT_SURVEY": 92.0,
            "STAT_LABOUR": 88.0,
            "STAT_QUALITY": 85.0,
            "STAT_IND_AGRI": 80.0,
            "STAT_DATA_GOV": 75.0,
            "STAT_COMPUTE": 75.0,
            "STAT_PRICE_IND": 75.0,
            "STAT_NAT_ACC": 70.0,
            "STAT_VIZ_COMM": 70.0
        },
        "weights": {
            "STAT_SURVEY": 1.5,
            "STAT_LABOUR": 1.4,
            "STAT_QUALITY": 1.3,
            "STAT_IND_AGRI": 1.2,
            "STAT_DATA_GOV": 1.0,
            "STAT_COMPUTE": 1.0,
            "STAT_PRICE_IND": 1.0,
            "STAT_NAT_ACC": 0.8,
            "STAT_VIZ_COMM": 0.8
        }
    },
    "MoSPI Economic Statistics Division (ESD)": {
        "division_code": "ESD",
        "description": "Compilation of Consumer Price Index (CPI), Index of Industrial Production (IIP), and Annual Survey of Industries.",
        "core_competencies": ["STAT_PRICE_IND", "STAT_IND_AGRI", "STAT_COMPUTE", "STAT_QUALITY", "STAT_NAT_ACC"],
        "benchmarks": {
            "STAT_PRICE_IND": 92.0,
            "STAT_IND_AGRI": 88.0,
            "STAT_COMPUTE": 82.0,
            "STAT_QUALITY": 82.0,
            "STAT_NAT_ACC": 80.0,
            "STAT_DATA_GOV": 78.0,
            "STAT_SURVEY": 75.0,
            "STAT_LABOUR": 72.0,
            "STAT_VIZ_COMM": 75.0
        },
        "weights": {
            "STAT_PRICE_IND": 1.5,
            "STAT_IND_AGRI": 1.4,
            "STAT_COMPUTE": 1.2,
            "STAT_QUALITY": 1.2,
            "STAT_NAT_ACC": 1.1,
            "STAT_DATA_GOV": 1.0,
            "STAT_SURVEY": 0.9,
            "STAT_LABOUR": 0.9,
            "STAT_VIZ_COMM": 0.9
        }
    },
    "MoSPI Survey Design & Research Division (SDRD)": {
        "division_code": "SDRD",
        "description": "Design of sampling frames, questionnaire formulation, estimation procedures, and survey research manuals.",
        "core_competencies": ["STAT_SURVEY", "STAT_COMPUTE", "STAT_QUALITY", "STAT_LABOUR", "STAT_VIZ_COMM"],
        "benchmarks": {
            "STAT_SURVEY": 95.0,
            "STAT_COMPUTE": 88.0,
            "STAT_QUALITY": 88.0,
            "STAT_LABOUR": 82.0,
            "STAT_VIZ_COMM": 80.0,
            "STAT_DATA_GOV": 80.0,
            "STAT_NAT_ACC": 72.0,
            "STAT_PRICE_IND": 72.0,
            "STAT_IND_AGRI": 72.0
        },
        "weights": {
            "STAT_SURVEY": 1.6,
            "STAT_COMPUTE": 1.3,
            "STAT_QUALITY": 1.3,
            "STAT_LABOUR": 1.1,
            "STAT_VIZ_COMM": 1.0,
            "STAT_DATA_GOV": 1.0,
            "STAT_NAT_ACC": 0.8,
            "STAT_PRICE_IND": 0.8,
            "STAT_IND_AGRI": 0.8
        }
    },
    "MoSPI Data Quality & Dissemination Division (DQDD)": {
        "division_code": "DQDD",
        "description": "eSankhyiki management, open microdata dissemination, SDG indicators, metadata standards, and data auditing.",
        "core_competencies": ["STAT_DATA_GOV", "STAT_VIZ_COMM", "STAT_QUALITY", "STAT_COMPUTE", "STAT_SURVEY"],
        "benchmarks": {
            "STAT_DATA_GOV": 92.0,
            "STAT_VIZ_COMM": 90.0,
            "STAT_QUALITY": 88.0,
            "STAT_COMPUTE": 85.0,
            "STAT_SURVEY": 78.0,
            "STAT_NAT_ACC": 75.0,
            "STAT_PRICE_IND": 75.0,
            "STAT_LABOUR": 75.0,
            "STAT_IND_AGRI": 72.0
        },
        "weights": {
            "STAT_DATA_GOV": 1.5,
            "STAT_VIZ_COMM": 1.4,
            "STAT_QUALITY": 1.3,
            "STAT_COMPUTE": 1.2,
            "STAT_SURVEY": 1.0,
            "STAT_NAT_ACC": 0.9,
            "STAT_PRICE_IND": 0.9,
            "STAT_LABOUR": 0.9,
            "STAT_IND_AGRI": 0.8
        }
    },
    "State DES (Directorate of Economics & Statistics)": {
        "division_code": "DES",
        "description": "State domestic product (GSDP), district-level statistics, local price collection, and state statistical coordination.",
        "core_competencies": ["STAT_SURVEY", "STAT_PRICE_IND", "STAT_NAT_ACC", "STAT_DATA_GOV", "STAT_IND_AGRI"],
        "benchmarks": {
            "STAT_SURVEY": 85.0,
            "STAT_PRICE_IND": 85.0,
            "STAT_NAT_ACC": 82.0,
            "STAT_DATA_GOV": 78.0,
            "STAT_IND_AGRI": 78.0,
            "STAT_QUALITY": 78.0,
            "STAT_COMPUTE": 75.0,
            "STAT_LABOUR": 75.0,
            "STAT_VIZ_COMM": 72.0
        },
        "weights": {
            "STAT_SURVEY": 1.3,
            "STAT_PRICE_IND": 1.3,
            "STAT_NAT_ACC": 1.2,
            "STAT_DATA_GOV": 1.1,
            "STAT_IND_AGRI": 1.1,
            "STAT_QUALITY": 1.0,
            "STAT_COMPUTE": 1.0,
            "STAT_LABOUR": 0.9,
            "STAT_VIZ_COMM": 0.9
        }
    },
    "Ministry Line Department / NITI Aayog": {
        "division_code": "POLICY",
        "description": "Policy analytics, Sustainable Development Goal tracking, inter-ministerial data coordination, and official reporting.",
        "core_competencies": ["STAT_VIZ_COMM", "STAT_DATA_GOV", "STAT_NAT_ACC", "STAT_QUALITY", "STAT_COMPUTE"],
        "benchmarks": {
            "STAT_VIZ_COMM": 90.0,
            "STAT_DATA_GOV": 85.0,
            "STAT_NAT_ACC": 85.0,
            "STAT_QUALITY": 82.0,
            "STAT_COMPUTE": 80.0,
            "STAT_SURVEY": 75.0,
            "STAT_PRICE_IND": 75.0,
            "STAT_LABOUR": 75.0,
            "STAT_IND_AGRI": 72.0
        },
        "weights": {
            "STAT_VIZ_COMM": 1.5,
            "STAT_DATA_GOV": 1.3,
            "STAT_NAT_ACC": 1.3,
            "STAT_QUALITY": 1.1,
            "STAT_COMPUTE": 1.1,
            "STAT_SURVEY": 0.9,
            "STAT_PRICE_IND": 0.9,
            "STAT_LABOUR": 0.9,
            "STAT_IND_AGRI": 0.8
        }
    }
}

DESIGNATION_MODIFIERS = {
    "Director General": {"benchmark_delta": 7.0, "weight_multiplier": 1.20, "seniority": "Senior Leadership", "role_category": "senior", "target_difficulty": "Expert"},
    "Director": {"benchmark_delta": 6.0, "weight_multiplier": 1.15, "seniority": "Senior Leadership", "role_category": "senior", "target_difficulty": "Advanced"},
    "Joint Director": {"benchmark_delta": 5.0, "weight_multiplier": 1.12, "seniority": "Senior Leadership", "role_category": "senior", "target_difficulty": "Advanced"},
    "Dy. Director": {"benchmark_delta": 4.0, "weight_multiplier": 1.10, "seniority": "Middle Management", "role_category": "mid", "target_difficulty": "Intermediate"},
    "Deputy Director": {"benchmark_delta": 4.0, "weight_multiplier": 1.10, "seniority": "Middle Management", "role_category": "mid", "target_difficulty": "Intermediate"},
    "Assistant Director": {"benchmark_delta": 2.0, "weight_multiplier": 1.05, "seniority": "Junior Cadre Leadership", "role_category": "mid", "target_difficulty": "Intermediate"},
    "Senior Statistical Officer": {"benchmark_delta": 2.0, "weight_multiplier": 1.05, "seniority": "Technical Supervisory", "role_category": "mid", "target_difficulty": "Intermediate"},
    "SSO": {"benchmark_delta": 2.0, "weight_multiplier": 1.05, "seniority": "Technical Supervisory", "role_category": "mid", "target_difficulty": "Intermediate"},
    "Junior Statistical Officer": {"benchmark_delta": 0.0, "weight_multiplier": 1.00, "seniority": "Technical Operations", "role_category": "junior", "target_difficulty": "Foundational"},
    "JSO": {"benchmark_delta": 0.0, "weight_multiplier": 1.00, "seniority": "Technical Operations", "role_category": "junior", "target_difficulty": "Foundational"},
    "Statistical Investigator": {"benchmark_delta": -2.0, "weight_multiplier": 0.95, "seniority": "Field Execution", "role_category": "junior", "target_difficulty": "Foundational"},
    "Investigator": {"benchmark_delta": -2.0, "weight_multiplier": 0.95, "seniority": "Field Execution", "role_category": "junior", "target_difficulty": "Foundational"},
    "Field Officer": {"benchmark_delta": -2.0, "weight_multiplier": 0.95, "seniority": "Field Execution", "role_category": "junior", "target_difficulty": "Foundational"},
    "Data Analyst": {"benchmark_delta": 2.0, "weight_multiplier": 1.05, "seniority": "Analytical Technical", "role_category": "technical", "target_difficulty": "Advanced"},
    "Data Scientist": {"benchmark_delta": 4.0, "weight_multiplier": 1.10, "seniority": "Advanced Data Science", "role_category": "technical", "target_difficulty": "Advanced"},
    "Database Administrator": {"benchmark_delta": 2.0, "weight_multiplier": 1.05, "seniority": "Data Engineering & Systems", "role_category": "technical", "target_difficulty": "Intermediate"}
}

DEPARTMENT_BASELINE_BANK = {
    "NAD": [
        {
            "id": 101,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Advanced",
            "question_text": "In the National Accounts Division (NAD) compilation under SNA 2008, how is Gross Value Added (GVA) at basic prices converted into GDP at market prices?",
            "options": [
                {"key": "A", "text": "Add Product Taxes and subtract Product Subsidies"},
                {"key": "B", "text": "Subtract Production Taxes and add Production Subsidies"},
                {"key": "C", "text": "Add Direct Income Taxes and subtract Net Exports"},
                {"key": "D", "text": "Add Net Factor Income from Abroad"}
            ],
            "correct_option": "A",
            "explanation": "Under SNA 2008, GDP at market prices = GVA at basic prices + Product Taxes - Product Subsidies."
        },
        {
            "id": 102,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Advanced",
            "question_text": "Which account in the SNA 2008 sequence of accounts records the allocation of primary income to institutional sectors?",
            "options": [
                {"key": "A", "text": "Production Account"},
                {"key": "B", "text": "Primary Distribution of Income Account"},
                {"key": "C", "text": "Use of Disposable Income Account"},
                {"key": "D", "text": "Capital Account"}
            ],
            "correct_option": "B",
            "explanation": "The Allocation of Primary Income Account shows resident institutional units as recipients of primary income derived from production."
        },
        {
            "id": 103,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "question_text": "For NAD macro-data wrangling, what is the primary purpose of integrating MCA-21 administrative company data into GDP estimation?",
            "options": [
                {"key": "A", "text": "Replacing field sample surveys completely with direct corporate balance sheet aggregations"},
                {"key": "B", "text": "Capturing real-time corporate financial performance for organized manufacturing and services GVA"},
                {"key": "C", "text": "Calculating individual corporate tax liabilities"},
                {"key": "D", "text": "Determining annual consumer price inflation"}
            ],
            "correct_option": "B",
            "explanation": "MCA-21 database filing analysis provides financial data for thousands of active enterprise balance sheets to estimate corporate GVA."
        },
        {
            "id": 104,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "question_text": "When deflating nominal GVA series to obtain real GDP at constant basic prices in NAD, which index series is primary for intermediate consumption?",
            "options": [
                {"key": "A", "text": "Consumer Price Index (Combined)"},
                {"key": "B", "text": "Wholesale Price Index (WPI) item-specific deflators"},
                {"key": "C", "text": "Index of Industrial Production (IIP)"},
                {"key": "D", "text": "Gold & Foreign Exchange Price Index"}
            ],
            "correct_option": "B",
            "explanation": "In double deflation or single deflation of input costs, relevant sub-indices of WPI and CPI are applied to convert current price inputs to constant price series."
        },
        {
            "id": 105,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "Under the UN System of National Accounts standards followed by MoSPI, what is the recommended practice for Supply and Use Tables (SUT)?",
            "options": [
                {"key": "A", "text": "Balancing total supply of goods and services with total use across all commodity groups"},
                {"key": "B", "text": "Ignoring import and export flows in national commodity balances"},
                {"key": "C", "text": "Relying exclusively on unverified informal sector sample estimates"},
                {"key": "D", "text": "Fixing intermediate consumption ratios without periodic update"}
            ],
            "correct_option": "A",
            "explanation": "Supply and Use Tables reconcile product supply (output + imports) with product use (intermediate + final consumption + exports + capital formation)."
        },
        {
            "id": 106,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Intermediate",
            "question_text": "How does eSankhyiki's Macro Indicators Module serve National Accounts Division data consumers?",
            "options": [
                {"key": "A", "text": "Providing interactive time-series queries and machine-readable REST APIs for GDP, GVA, and Gross Capital Formation"},
                {"key": "B", "text": "Restricting GDP data access to registered commercial banks only"},
                {"key": "C", "text": "Hosting raw un-anonymized household tax records"},
                {"key": "D", "text": "Managing internal officer transfers"}
            ],
            "correct_option": "A",
            "explanation": "eSankhyiki Macro Indicators module provides filtered, open time-series access and REST APIs for national accounts aggregates."
        },
        {
            "id": 107,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "question_text": "How are NSS unincorporated enterprise survey results utilized in National Accounts compilation?",
            "options": [
                {"key": "A", "text": "To benchmark GVA per worker estimates for the unorganized manufacturing and services sectors"},
                {"key": "B", "text": "To calculate national debt service obligations"},
                {"key": "C", "text": "To determine municipal property tax rates"},
                {"key": "D", "text": "To set central bank interest rates"}
            ],
            "correct_option": "A",
            "explanation": "Unincorporated enterprise surveys provide value added per worker benchmarks to estimate informal sector contribution to GVA."
        },
        {
            "id": 108,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "Which metric from Periodic Labour Force Survey (PLFS) is critical for estimating informal sector workforce in National Accounts?",
            "options": [
                {"key": "A", "text": "Worker Population Ratio (WPR) categorized by Usual Principal & Subsidiary Status (UPSS)"},
                {"key": "B", "text": "Monthly gross wage inflation rates only"},
                {"key": "C", "text": "International migration counts"},
                {"key": "D", "text": "Total pensioner enrollment counts"}
            ],
            "correct_option": "A",
            "explanation": "PLFS UPSS workforce estimates are combined with survey-based GVA per worker to compute total unorganized sector GVA."
        },
        {
            "id": 109,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "question_text": "In NAD compilation, how is organized manufacturing GVA reconciled between ASI and MCA-21 database sources?",
            "options": [
                {"key": "A", "text": "ASI factory census results are cross-validated against corporate MCA-21 financial reports to avoid double counting"},
                {"key": "B", "text": "ASI data is discarded entirely"},
                {"key": "C", "text": "MCA-21 data is multiplied by a fixed factor of 10"},
                {"key": "D", "text": "Factory output is estimated without input deductions"}
            ],
            "correct_option": "A",
            "explanation": "Organized manufacturing compilation cross-validates ASI factory census data and corporate MCA-21 balance sheets for benchmark consistency."
        }
    ],
    "FOD": [
        {
            "id": 201,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "question_text": "For Field Operations Division (FOD) officers conducting NSS rural household surveys, what constitutes the First Stage Unit (FSU)?",
            "options": [
                {"key": "A", "text": "Census Villages (or sub-units in large villages)"},
                {"key": "B", "text": "Individual households"},
                {"key": "C", "text": "Gram Panchayat Chairpersons"},
                {"key": "D", "text": "State Administrative Capital Cities"}
            ],
            "correct_option": "A",
            "explanation": "In rural areas, census villages serve as FSUs, from which sample households (Ultimate Stage Units) are selected."
        },
        {
            "id": 202,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "During PLFS field canvassing by FOD investigators, how is an individual classified as 'Employed' under Current Weekly Status (CWS)?",
            "options": [
                {"key": "A", "text": "Worked for at least 1 hour on any 1 day during the 7-day reference period"},
                {"key": "B", "text": "Worked for at least 183 days during the preceding year"},
                {"key": "C", "text": "Worked continuous 8-hour shifts for all 7 days"},
                {"key": "D", "text": "Was actively seeking work throughout the last month"}
            ],
            "correct_option": "A",
            "explanation": "Under CWS, working for at least 1 hour on any day during the 7-day reference period qualifies a person as employed."
        },
        {
            "id": 203,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "What is the primary role of Supervisory Officers in FOD field survey operations to minimize non-sampling error?",
            "options": [
                {"key": "A", "text": "Conducting independent supervisory re-checks, concurrent field inspections, and schedule audit validation"},
                {"key": "B", "text": "Filling out schedules without visiting households"},
                {"key": "C", "text": "Replacing random sampling with convenience sampling"},
                {"key": "D", "text": "Changing sampling multipliers arbitrarily"}
            ],
            "correct_option": "A",
            "explanation": "Supervisory re-inspection and schedule audits ensure high data accuracy and minimize non-sampling errors."
        },
        {
            "id": 204,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "question_text": "During Annual Survey of Industries (ASI) field visits by FOD officers, what physical documentation is inspected at registered factory units?",
            "options": [
                {"key": "A", "text": "Audited balance sheets, profit & loss accounts, employment registers, and fuel/power records"},
                {"key": "B", "text": "Worker personal bank passbooks only"},
                {"key": "C", "text": "Municipal water utility bills exclusively"},
                {"key": "D", "text": "Unverified verbal statements"}
            ],
            "correct_option": "A",
            "explanation": "ASI canvassing requires verifying audited financial statements, output registers, and input records from factory books."
        },
        {
            "id": 205,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Intermediate",
            "question_text": "How has the adoption of CAPI (Computer Assisted Personal Interviewing) handheld tablets changed FOD field data collection?",
            "options": [
                {"key": "A", "text": "Enables real-time data entry validation, geo-tagging, and immediate transmission to headquarters server"},
                {"key": "B", "text": "Eliminates the need for field investigators completely"},
                {"key": "C", "text": "Replaces household visits with social media surveys"},
                {"key": "D", "text": "Prevents data validation checks entirely"}
            ],
            "correct_option": "A",
            "explanation": "CAPI tablets incorporate built-in validation rules, timestamping, and immediate sync with central processing servers."
        },
        {
            "id": 206,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "question_text": "In FOD data processing, why is validating unit-level multiplier flags critical before uploading survey batch files?",
            "options": [
                {"key": "A", "text": "Incorrect multiplier values distort population estimates during weighted sample aggregation"},
                {"key": "B", "text": "Multipliers determine investigator salary rates"},
                {"key": "C", "text": "Multipliers are only used for graphic display titles"},
                {"key": "D", "text": "Multipliers automatically delete non-responsive households"}
            ],
            "correct_option": "A",
            "explanation": "Sampling multipliers expand sample unit records into population totals; incorrect values corrupt weighted aggregate estimates."
        },
        {
            "id": 207,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "question_text": "In monthly CPI price collection undertaken by FOD field staff, what is the protocol if a selected item specification is temporarily missing in a market?",
            "options": [
                {"key": "A", "text": "Collect price of comparable substitute item and document specification change as per ESD SOP"},
                {"key": "B", "text": "Enter zero price for the month"},
                {"key": "C", "text": "Double the price of a completely unrelated item"},
                {"key": "D", "text": "Skip visiting the market entirely"}
            ],
            "correct_option": "A",
            "explanation": "Standard operating procedure requires collecting prices for comparable substitute items or applying specified cell imputation rules."
        },
        {
            "id": 208,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "How does accurate field listing of unorganized enterprise units by FOD support National Accounts Statistics?",
            "options": [
                {"key": "A", "text": "Provides reliable sampling frames for enterprise surveys that feed into unorganized sector GVA"},
                {"key": "B", "text": "Determines central tax collection rates"},
                {"key": "C", "text": "Calculates foreign exchange reserves"},
                {"key": "D", "text": "Replaces national census operations"}
            ],
            "correct_option": "A",
            "explanation": "Field listing provides the updated frame necessary for drawing representative enterprise samples used in National Accounts."
        },
        {
            "id": 209,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Intermediate",
            "question_text": "Why is reporting non-response rates and field casualty numbers crucial in FOD survey progress reports?",
            "options": [
                {"key": "A", "text": "Allows survey statisticians to assess potential non-response bias and adjust final sampling weights"},
                {"key": "B", "text": "Non-response figures are kept confidential and never documented"},
                {"key": "C", "text": "Non-response automatically invalidates the entire survey round"},
                {"key": "D", "text": "Field casualty numbers are only used for vehicle mileage billing"}
            ],
            "correct_option": "A",
            "explanation": "Documenting non-response rates enables calculating non-response weight adjustments to preserve sample representativeness."
        }
    ],
    "ESD": [
        {
            "id": 301,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Advanced",
            "question_text": "In Economic Statistics Division (ESD) compilation of headline CPI (Combined), which index formulation is used for item aggregation across base weights?",
            "options": [
                {"key": "A", "text": "Laspeyres Base Weighted Formula"},
                {"key": "B", "text": "Paasche Current Weighted Formula"},
                {"key": "C", "text": "Fisher's Ideal Geometric Index"},
                {"key": "D", "text": "Simple Unweighted Arithmetic Mean"}
            ],
            "correct_option": "A",
            "explanation": "Headline CPI is compiled using a modified Laspeyres base-weighted index formula with fixed item expenditure weights."
        },
        {
            "id": 302,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Advanced",
            "question_text": "In the Annual Survey of Industries (ASI) compiled by ESD, what constitutes the Census Sector of the factory frame?",
            "options": [
                {"key": "A", "text": "Units employing 100 or more workers (or 50 or more in select states) surveyed on 100% enumeration basis"},
                {"key": "B", "text": "Small household cottage industries only"},
                {"key": "C", "text": "Agricultural farming holdings above 5 hectares"},
                {"key": "D", "text": "Units operating exclusively in export processing zones"}
            ],
            "correct_option": "A",
            "explanation": "The ASI frame is split into Census Sector (large factories surveyed 100%) and Sample Sector (smaller factories sample-surveyed)."
        },
        {
            "id": 303,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "question_text": "When processing monthly Index of Industrial Production (IIP) item group returns, how are missing factory production figures imputed in ESD pipelines?",
            "options": [
                {"key": "A", "text": "Using item-level growth rate of responding units or historical trend moving average"},
                {"key": "B", "text": "Setting missing values to zero permanently"},
                {"key": "C", "text": "Multiplying the base year weight by 100"},
                {"key": "D", "text": "Replacing production values with factory worker counts"}
            ],
            "correct_option": "A",
            "explanation": "Standard IIP compilation imputes missing monthly factory returns using growth rates of responding units in the same item group."
        },
        {
            "id": 304,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "What quality assurance mechanism is enforced by ESD before releasing monthly CPI and IIP indices?",
            "options": [
                {"key": "A", "text": "Multi-stage automated outlier checks, price quotation verification, and supervisory validation committee sign-off"},
                {"key": "B", "text": "Releasing provisional data without checking price quotes"},
                {"key": "C", "text": "Subcontracting index calculations to external commercial firms"},
                {"key": "D", "text": "Publishing figures exclusively on paper printouts"}
            ],
            "correct_option": "A",
            "explanation": "ESD applies automated outlier detection and multi-level technical reviews prior to official index release."
        },
        {
            "id": 305,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "How are ESD industrial statistics (ASI Net Value Added) integrated into National Accounts GDP compilation?",
            "options": [
                {"key": "A", "text": "ASI Net Value Added forms the empirical benchmark for organized manufacturing GVA"},
                {"key": "B", "text": "ASI data is ignored in national accounts"},
                {"key": "C", "text": "ASI figures are used only for agricultural output"},
                {"key": "D", "text": "ASI data replaces central government budget accounts"}
            ],
            "correct_option": "A",
            "explanation": "ASI Net Value Added is a fundamental empirical building block for manufacturing sector GVA in National Accounts."
        },
        {
            "id": 306,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Intermediate",
            "question_text": "What is the official dissemination protocol for monthly CPI and IIP releases by ESD?",
            "options": [
                {"key": "A", "text": "Synchronous release at 4:00 PM on designated release days via eSankhyiki portal and press note"},
                {"key": "B", "text": "Staggered release over 30 days without scheduled calendar"},
                {"key": "C", "text": "Restricted distribution to private subscription clients only"},
                {"key": "D", "text": "Oral briefing without digital data files"}
            ],
            "correct_option": "A",
            "explanation": "Monthly CPI and IIP indices are released strictly per the advance release calendar on the official portal at 4:00 PM."
        },
        {
            "id": 307,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "question_text": "In selecting factory units for the ASI Sample Sector, what sampling scheme is employed by ESD and SDRD?",
            "options": [
                {"key": "A", "text": "Circular systematic sampling within stratified state-by-NIC 4-digit strata"},
                {"key": "B", "text": "Simple random sampling without stratification"},
                {"key": "C", "text": "Convenience sampling of factories near highway corridors"},
                {"key": "D", "text": "Selecting only government-owned state enterprises"}
            ],
            "correct_option": "A",
            "explanation": "The ASI Sample Sector uses stratified circular systematic sampling within State x NIC 4-digit industry strata."
        },
        {
            "id": 308,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "What key labor metrics are compiled from ASI factory returns by ESD?",
            "options": [
                {"key": "A", "text": "Total persons engaged, mandays worked, wages/salaries paid, and bonus contributions"},
                {"key": "B", "text": "Agricultural labor wage rates only"},
                {"key": "C", "text": "Civil servant retirement counts"},
                {"key": "D", "text": "School enrollment metrics"}
            ],
            "correct_option": "A",
            "explanation": "ASI compiles detailed labor indicators including employees, workers, mandays worked, and total compensation."
        },
        {
            "id": 309,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Intermediate",
            "question_text": "Why are item-level weighting diagrams published alongside CPI base year revisions by ESD?",
            "options": [
                {"key": "A", "text": "To ensure public transparency and enable policy analysts to verify commodity basket shares"},
                {"key": "B", "text": "To hide inflation calculation methods"},
                {"key": "C", "text": "Weighting diagrams are internal secret documents"},
                {"key": "D", "text": "To satisfy commercial marketing requirements"}
            ],
            "correct_option": "A",
            "explanation": "Publishing CPI weighting diagrams ensures complete methodological transparency under official statistical standards."
        }
    ],
    "SDRD": [
        {
            "id": 401,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Advanced",
            "question_text": "In Survey Design & Research Division (SDRD) sampling design, what is the principal objective of stratification in multi-stage surveys?",
            "options": [
                {"key": "A", "text": "Maximizing variance between strata and minimizing variance within strata to increase estimation precision"},
                {"key": "B", "text": "Eliminating the need for sampling weights"},
                {"key": "C", "text": "Reducing the total number of survey questions"},
                {"key": "D", "text": "Guaranteeing 100% sample inclusion for all households"}
            ],
            "correct_option": "A",
            "explanation": "Stratification groups similar units into homogeneous sub-populations to minimize within-stratum variance and reduce standard error."
        },
        {
            "id": 402,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Advanced",
            "question_text": "In SDRD survey estimation pipelines, how is the Relative Standard Error (RSE) calculated for a domain total estimate?",
            "options": [
                {"key": "A", "text": "RSE (%) = (Standard Error of Estimate / Estimated Total) * 100"},
                {"key": "B", "text": "RSE (%) = (Sample Size / Population Total) * 100"},
                {"key": "C", "text": "RSE (%) = (Unweighted Mean / Weighted Mean) * 100"},
                {"key": "D", "text": "RSE (%) = Maximum Value - Minimum Value"}
            ],
            "correct_option": "A",
            "explanation": "Relative Standard Error measures estimate precision by expressing standard error as a percentage of the estimated total."
        },
        {
            "id": 403,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "What design strategy does SDRD use in PLFS household rotation panels to control recall bias and urban attrition?",
            "options": [
                {"key": "A", "text": "Rotational panel design with 25% sample replacement each quarter in urban areas"},
                {"key": "B", "text": "Replacing 100% of urban sample households every week"},
                {"key": "C", "text": "Surveying the exact same households indefinitely without rotation"},
                {"key": "D", "text": "Using unverified telephone surveys"}
            ],
            "correct_option": "A",
            "explanation": "PLFS urban panel uses a 75% overlap rotational scheme across 4 visits to balance panel attrition and trend estimation."
        },
        {
            "id": 404,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "In SDRD questionnaire formulation for PLFS, what is the distinction between Usual Principal Status (UPS) and Subsidiary Economic Activity Status (SS)?",
            "options": [
                {"key": "A", "text": "UPS is major time spent (>= 183 days) during 365 days; SS is secondary economic activity of at least 30 days"},
                {"key": "B", "text": "UPS is weekly activity; SS is daily activity"},
                {"key": "C", "text": "UPS applies only to urban areas; SS applies only to rural areas"},
                {"key": "D", "text": "UPS measures pension status; SS measures formal salary status"}
            ],
            "correct_option": "A",
            "explanation": "UPS captures the principal activity pursued for the majority of the reference year; SS captures secondary economic work of >= 30 days."
        },
        {
            "id": 405,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Intermediate",
            "question_text": "What technical document is authored by SDRD upon completion of survey design for field implementation by FOD?",
            "options": [
                {"key": "A", "text": "Instructions to Field Investigators & Concepts/Definitions Manual (Schedule Manual)"},
                {"key": "B", "text": "Central Government Budget Speech"},
                {"key": "C", "text": "Commercial Marketing Pamphlet"},
                {"key": "D", "text": "Annual Import Customs Duty Gazette"}
            ],
            "correct_option": "A",
            "explanation": "SDRD authors the comprehensive Schedule Manual detailing concepts, field definitions, and item-by-item instructions."
        },
        {
            "id": 406,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Intermediate",
            "question_text": "What anonymization standards are specified by SDRD for public microdata dissemination on eSankhyiki?",
            "options": [
                {"key": "A", "text": "Top-coding extreme income/expenditure values, suppressing micro-geographic identifiers, and k-anonymity masking"},
                {"key": "B", "text": "Publishing full names, Aadhaar numbers, and phone numbers"},
                {"key": "C", "text": "Withholding all microdata from academic researchers permanently"},
                {"key": "D", "text": "Encrypting microdata files without decryption keys"}
            ],
            "correct_option": "A",
            "explanation": "SDRD anonymization protocols mandate top-coding, masking geographic sub-districts, and removing direct identifiers."
        },
        {
            "id": 407,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "How does SDRD align Household Consumption Expenditure Survey (HCES) schedules with SNA 2008 requirements?",
            "options": [
                {"key": "A", "text": "Structuring item classifications to match COICOP (Classification of Individual Consumption According to Purpose)"},
                {"key": "B", "text": "Excluding all non-food items from the survey schedule"},
                {"key": "C", "text": "Measuring only corporate inventory investments"},
                {"key": "D", "text": "Replacing household items with wholesale trade commodities"}
            ],
            "correct_option": "A",
            "explanation": "HCES items are aligned with international COICOP standards to support National Accounts private consumption expenditure estimation."
        },
        {
            "id": 408,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "question_text": "What role does SDRD's Household Consumption Expenditure Survey play in CPI compilation?",
            "options": [
                {"key": "A", "text": "Provides consumer expenditure basket weighting diagrams for rural, urban, and combined CPI series"},
                {"key": "B", "text": "Determines monthly Wholesale Price Index quote figures"},
                {"key": "C", "text": "Sets factory production quota targets"},
                {"key": "D", "text": "Measures foreign exchange inflation rate"}
            ],
            "correct_option": "A",
            "explanation": "HCES consumption expenditure shares form the empirical weighting diagram for Consumer Price Index base year revisions."
        },
        {
            "id": 409,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "question_text": "How does SDRD design sampling frames for unincorporated enterprise surveys (ASUSE)?",
            "options": [
                {"key": "A", "text": "Multi-stage stratified sampling using Economic Census / EC frame and urban frame blocks as FSUs"},
                {"key": "B", "text": "Selecting factories exclusively from stock exchange listings"},
                {"key": "C", "text": "Sampling agricultural farms over 50 acres only"},
                {"key": "D", "text": "Convenience sampling at district headquarter markets"}
            ],
            "correct_option": "A",
            "explanation": "Unincorporated enterprise surveys utilize Economic Census unit frames and sample clusters to capture informal activity."
        }
    ],
    "DQDD": [
        {
            "id": 501,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Advanced",
            "question_text": "In Data Quality & Dissemination Division (DQDD) operations, what is the primary objective of the eSankhyiki portal microdata repository?",
            "options": [
                {"key": "A", "text": "Providing open, FAIR-compliant, anonymized microdata schedules and macro indicators for researchers and public"},
                {"key": "B", "text": "Selling government data to commercial advertisers"},
                {"key": "C", "text": "Storing unencrypted confidential officer records"},
                {"key": "D", "text": "Hosting private commercial software downloads"}
            ],
            "correct_option": "A",
            "explanation": "eSankhyiki is MoSPI's official open data portal delivering FAIR-aligned statistical indicators and microdata."
        },
        {
            "id": 502,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Advanced",
            "question_text": "How does DQDD manage the Sustainable Development Goal (SDG) National Indicator Framework (NIF) dashboard?",
            "options": [
                {"key": "A", "text": "Tracks baseline-to-target indicator trends across States/UTs with interactive policy charts and metadata standards"},
                {"key": "B", "text": "Restricts viewing of state rankings to central ministers only"},
                {"key": "C", "text": "Replaces quantitative indicators with qualitative news stories"},
                {"key": "D", "text": "Monitors private corporate stock performance"}
            ],
            "correct_option": "A",
            "explanation": "The SDG NIF dashboard visualizes multi-sector indicators to track state and national progress toward 2030 targets."
        },
        {
            "id": 503,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "Which framework forms the basis for DQDD's statistical audit checklists for official datasets?",
            "options": [
                {"key": "A", "text": "UN National Quality Assurance Framework (NQAF) and Fundamental Principles of Official Statistics"},
                {"key": "B", "text": "Commercial ISO 9001 factory manufacturing standard"},
                {"key": "C", "text": "Private banking credit rating guidelines"},
                {"key": "D", "text": "Unwritten departmental traditions"}
            ],
            "correct_option": "A",
            "explanation": "MoSPI's quality assurance framework is aligned with UN NQAF standards for official statistical systems."
        },
        {
            "id": 504,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "question_text": "What API standard is implemented on eSankhyiki by DQDD for automated data ingestion by external applications?",
            "options": [
                {"key": "A", "text": "RESTful JSON APIs with metadata headers and OpenAPI specification"},
                {"key": "B", "text": "Proprietary binary file formats without documentation"},
                {"key": "C", "text": "Manual paper fax requests only"},
                {"key": "D", "text": "FTP download requiring physical dongle key"}
            ],
            "correct_option": "A",
            "explanation": "eSankhyiki Macro Indicators module provides standard REST APIs with JSON payloads for seamless data integration."
        },
        {
            "id": 505,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "question_text": "What metadata documentation must accompany every unit-record microdata release validated by DQDD?",
            "options": [
                {"key": "A", "text": "Data dictionary, schedule layout, sampling design note, estimation procedure, and multiplier variable definition"},
                {"key": "B", "text": "Raw code without variable labels"},
                {"key": "C", "text": "Only total sample size count"},
                {"key": "D", "text": "Investigator personal contact numbers"}
            ],
            "correct_option": "A",
            "explanation": "Comprehensive microdata dissemination requires complete data dictionaries, sampling notes, and multiplier specifications."
        },
        {
            "id": 506,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "How does DQDD ensure temporal comparability of National Accounts data on eSankhyiki across base year revisions?",
            "options": [
                {"key": "A", "text": "Publishing linked back-series estimates alongside base year methodological documentation"},
                {"key": "B", "text": "Deleting older base year series from the portal"},
                {"key": "C", "text": "Modifying historic GDP figures without notes"},
                {"key": "D", "text": "Restricting access to historical series"}
            ],
            "correct_option": "A",
            "explanation": "Data governance best practices require maintaining linked back-series to preserve continuous macro time-series research."
        },
        {
            "id": 507,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "question_text": "What open data standard does DQDD enforce for time-series CPI and IIP data dissemination?",
            "options": [
                {"key": "A", "text": "Machine-readable CSV, JSON, and SDMX formats with standard metadata mapping"},
                {"key": "B", "text": "Non-copyable image PDF files only"},
                {"key": "C", "text": "Encrypted proprietary database files"},
                {"key": "D", "text": "Print-only postal circulars"}
            ],
            "correct_option": "A",
            "explanation": "Open government data guidelines mandate releasing statistical indicators in open, machine-readable formats (CSV, JSON, SDMX)."
        },
        {
            "id": 508,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "How are PLFS quarterly urban key indicators visualized on the DQDD data portal?",
            "options": [
                {"key": "A", "text": "Interactive trend dashboards breaking down LFPR, WPR, and UR across age groups and gender"},
                {"key": "B", "text": "Static single-page press releases without charts"},
                {"key": "C", "text": "Restricted internal memos"},
                {"key": "D", "text": "Raw un-aggregated text files"}
            ],
            "correct_option": "A",
            "explanation": "Dissemination portals provide interactive charts allowing users to filter labor metrics by demographic disaggregations."
        },
        {
            "id": 509,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "question_text": "What statistical disclosure control technique is applied by DQDD to ASI factory microdata to protect unit privacy?",
            "options": [
                {"key": "A", "text": "Suppressing direct factory identification numbers, state-NIC small cell counts, and top-coding capital aggregates"},
                {"key": "B", "text": "Releasing factory bank account numbers"},
                {"key": "C", "text": "Publishing un-sanitized factory owner names"},
                {"key": "D", "text": "Withholding all industrial data permanently"}
            ],
            "correct_option": "A",
            "explanation": "Protecting respondent confidentiality requires suppressing direct unit IDs and masking small cell counts."
        }
    ],
    "DES": [
        {
            "id": 601,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "In State Directorate of Economics & Statistics (DES), what aggregate is compiled to measure the state's total economic output?",
            "options": [
                {"key": "A", "text": "Gross State Domestic Product (GSDP) at basic and market prices"},
                {"key": "B", "text": "Central Union Budget Deficit"},
                {"key": "C", "text": "National Foreign Exchange Reserve"},
                {"key": "D", "text": "Total Municipal Water Tariff Collection"}
            ],
            "correct_option": "A",
            "explanation": "State DES compiles GSDP and Net State Domestic Product (NSDP) aligned with central NAD SNA 2008 guidelines."
        },
        {
            "id": 602,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "question_text": "What is the primary role of State DES field staff in price statistics compilation?",
            "options": [
                {"key": "A", "text": "Collecting weekly/monthly rural and urban retail prices from designated sample markets for state CPI"},
                {"key": "B", "text": "Setting retail shop price ceilings"},
                {"key": "C", "text": "Collecting international currency exchange rates"},
                {"key": "D", "text": "Managing state customs collection"}
            ],
            "correct_option": "A",
            "explanation": "State DES officers collect local market price quotations essential for compiling state Consumer Price Indices."
        },
        {
            "id": 603,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "question_text": "What is the 'State Sample' in NSS socio-economic survey rounds conducted by DES?",
            "options": [
                {"key": "A", "text": "An independent matching sample surveyed by DES staff using identical NSS schedules and design"},
                {"key": "B", "text": "A survey conducted without sampling frames"},
                {"key": "C", "text": "A sample consisting only of state government employees"},
                {"key": "D", "text": "An unverified opinion poll"}
            ],
            "correct_option": "A",
            "explanation": "State DES conducts matching state samples using identical NSS methodology to double overall sample size for pooling."
        },
        {
            "id": 604,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Intermediate",
            "question_text": "How does State DES coordinate data sharing with central MoSPI eSankhyiki platform?",
            "options": [
                {"key": "A", "text": "Transmitting state GSDP, district indicators, and local price series using standardized metadata formats"},
                {"key": "B", "text": "Keeping state data strictly isolated without central sharing"},
                {"key": "C", "text": "Selling state microdata to commercial brokers"},
                {"key": "D", "text": "De-standardizing indicator definitions"}
            ],
            "correct_option": "A",
            "explanation": "State-central statistical coordination ensures standardized metadata and seamless data flow between state portals and eSankhyiki."
        },
        {
            "id": 605,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "question_text": "How does State DES utilize Annual Survey of Industries (ASI) results at the state level?",
            "options": [
                {"key": "A", "text": "To estimate state manufacturing sector GSDP and evaluate regional industrial growth"},
                {"key": "B", "text": "To determine central income tax rates"},
                {"key": "C", "text": "To manage state transport bus fleets"},
                {"key": "D", "text": "To set central import tariffs"}
            ],
            "correct_option": "A",
            "explanation": "State ASI data provides empirical foundation for estimating organized manufacturing contribution to GSDP."
        },
        {
            "id": 606,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "What quality assurance step is critical when pooling Central and State NSS sample estimates?",
            "options": [
                {"key": "A", "text": "Testing statistical equality of central and state sample distributions before combining weights"},
                {"key": "B", "text": "Discarding central sample data automatically"},
                {"key": "C", "text": "Averaging unweighted state raw totals"},
                {"key": "D", "text": "Ignoring non-sampling differences"}
            ],
            "correct_option": "A",
            "explanation": "Pooling central and state samples requires rigorous statistical tests (Wald test / Kolmogorov-Smirnov) to verify distribution consistency."
        },
        {
            "id": 607,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "question_text": "In State DES statistical computing labs, how are district-level indicators processed efficiently?",
            "options": [
                {"key": "A", "text": "Using automated Python/R data wrangling scripts to aggregate microdata with district multipliers"},
                {"key": "B", "text": "Manual hand calculation on paper ledgers"},
                {"key": "C", "text": "Deleting all district records with missing values"},
                {"key": "D", "text": "Relying on unverified social media counts"}
            ],
            "correct_option": "A",
            "explanation": "Modern state DES offices utilize Python and R scripts to automate district microdata aggregation and quality checks."
        },
        {
            "id": 608,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "Why are state-level PLFS estimates vital for State DES policy planning?",
            "options": [
                {"key": "A", "text": "They provide state-specific Worker Population Ratios (WPR) and Unemployment Rates (UR) for state skill mission policies"},
                {"key": "B", "text": "They determine national defense recruitment targets"},
                {"key": "C", "text": "They replace state population census counts"},
                {"key": "D", "text": "They measure international diplomatic travel"}
            ],
            "correct_option": "A",
            "explanation": "State PLFS estimates guide state-level labor welfare schemes, vocational training, and employment planning."
        },
        {
            "id": 609,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Intermediate",
            "question_text": "What annual publication is compiled by State DES for state legislative budget presentations?",
            "options": [
                {"key": "A", "text": "State Economic Survey & District Statistical Handbooks"},
                {"key": "B", "text": "Central Railway Time Table"},
                {"key": "C", "text": "International Monetary Fund Annual Report"},
                {"key": "D", "text": "Private Commercial Bank Directory"}
            ],
            "correct_option": "A",
            "explanation": "State DES publishes the annual State Economic Survey summarizing GSDP growth, inflation, and sector performance for the state legislature."
        }
    ],
    "POLICY": [
        {
            "id": 701,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Advanced",
            "question_text": "In Ministry Line Departments and NITI Aayog policy analytics, how is the SDG India Index compiled from official statistical indicators?",
            "options": [
                {"key": "A", "text": "Normalizing target indicators to a 0-100 scale and computing composite goal scores across States and UTs"},
                {"key": "B", "text": "Ranking states based on total land area"},
                {"key": "C", "text": "Assigning equal 100 scores to all states regardless of data"},
                {"key": "D", "text": "Using unverified online poll votes"}
            ],
            "correct_option": "A",
            "explanation": "The SDG India Index normalizes official MoSPI/Ministry indicators to track progress across 16 SDGs for evidence-based policy benchmarking."
        },
        {
            "id": 702,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Advanced",
            "question_text": "What principle governs inter-ministerial data integration for evidence-based policy formulation?",
            "options": [
                {"key": "A", "text": "FAIR Principles (Findable, Accessible, Interoperable, Reusable) and National Data Sharing Policy (NDSAP)"},
                {"key": "B", "text": "Strict data isolation and total prohibition of inter-agency sharing"},
                {"key": "C", "text": "Selling government administrative data to private marketing vendors"},
                {"key": "D", "text": "Deleting administrative data after 30 days"}
            ],
            "correct_option": "A",
            "explanation": "Inter-ministerial policy coordination relies on FAIR principles and NDSAP standards to integrate administrative data silos."
        },
        {
            "id": 703,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "When policy analysts evaluate Gross Fixed Capital Formation (GFCF) trends in GDP data, what economic aspect are they assessing?",
            "options": [
                {"key": "A", "text": "Net additions to fixed assets and infrastructure investment in the economy"},
                {"key": "B", "text": "Short-term consumer grocery purchases"},
                {"key": "C", "text": "Government foreign diplomatic expenditure"},
                {"key": "D", "text": "Central bank currency printing volume"}
            ],
            "correct_option": "A",
            "explanation": "GFCF measures investment in fixed capital assets (buildings, machinery, infrastructure) driving long-term economic productive capacity."
        },
        {
            "id": 704,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Intermediate",
            "question_text": "Why must policy advisors inspect the sample design and standard error notes before citing survey findings?",
            "options": [
                {"key": "A", "text": "To verify that sample size and precision (RSE) support statistically significant policy conclusions"},
                {"key": "B", "text": "To change survey numbers to match political targets"},
                {"key": "C", "text": "Sample design notes have no relevance to policy"},
                {"key": "D", "text": "Standard errors are only used by software programmers"}
            ],
            "correct_option": "A",
            "explanation": "Policy decisions require checking estimate precision (RSE) and sample representation to avoid misleading generalizations."
        },
        {
            "id": 705,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "question_text": "How do data analysts in line ministries utilize Python/R for policy simulation models?",
            "options": [
                {"key": "A", "text": "Building reproducible econometric models, scenario forecasting, and automated policy report generation"},
                {"key": "B", "text": "Manually retyping tables into text documents"},
                {"key": "C", "text": "Replacing official survey data with random numbers"},
                {"key": "D", "text": "Running computer games during office hours"}
            ],
            "correct_option": "A",
            "explanation": "Data science tools allow scripting reproducible econometric models to evaluate prospective policy interventions."
        },
        {
            "id": 706,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "question_text": "Which PLFS metric is crucial for policy advisors designing youth employment and skill development schemes?",
            "options": [
                {"key": "A", "text": "Youth Unemployment Rate and NEET (Not in Employment, Education, or Training) percentage"},
                {"key": "B", "text": "Total senior citizen pension count"},
                {"key": "C", "text": "Agricultural land holding size"},
                {"key": "D", "text": "Commercial bank branch density"}
            ],
            "correct_option": "A",
            "explanation": "Youth unemployment rates and NEET metrics directly inform skill development policy and targeted employment schemes."
        },
        {
            "id": 707,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "question_text": "How should policy makers interpret a 95% confidence interval reported in an official NSS evaluation report?",
            "options": [
                {"key": "A", "text": "There is a 95% probability that the true population parameter lies within the calculated interval range"},
                {"key": "B", "text": "95% of the survey questionnaires were discarded"},
                {"key": "C", "text": "The survey results are 95% inaccurate"},
                {"key": "D", "text": "The survey cost 95% of the allocated budget"}
            ],
            "correct_option": "A",
            "explanation": "A 95% confidence interval provides the range within which the true population parameter is expected to fall with 95% confidence."
        },
        {
            "id": 708,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "question_text": "What inflation measure is monitored by NITI Aayog and Ministry of Finance for macroeconomic stability?",
            "options": [
                {"key": "A", "text": "Headline Consumer Price Index (Combined) year-on-year inflation rate and Core CPI inflation"},
                {"key": "B", "text": "Stock market index daily movement"},
                {"key": "C", "text": "Gold price futures index"},
                {"key": "D", "text": "Commercial real estate lease rates"}
            ],
            "correct_option": "A",
            "explanation": "Headline CPI and Core CPI (excluding volatile food/energy) guide monetary policy and cost-of-living indexation."
        },
        {
            "id": 709,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "question_text": "How do IIP growth rates inform industrial policy interventions by the Ministry of Commerce & Industry?",
            "options": [
                {"key": "A", "text": "Providing monthly early-warning signals on manufacturing, mining, and electricity sector output trends"},
                {"key": "B", "text": "Setting corporate income tax rates"},
                {"key": "C", "text": "Replacing annual financial audit reports"},
                {"key": "D", "text": "Determining individual factory worker salaries"}
            ],
            "correct_option": "A",
            "explanation": "IIP provides high-frequency monthly volume indicators to monitor industrial sector momentum and policy needs."
        }
    ]
}

COMMON_CORE_QUESTIONS = [
    {
        "id": 1,
        "competency_code": "STAT_SURVEY",
        "competency_name": "Survey Methodology & Sampling Design",
        "domain": "Survey Operations",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "In the National Sample Survey (NSS) multi-stage sampling design for rural areas, what generally serves as the First Stage Unit (FSU)?",
        "options": [
            {"key": "A", "text": "Individual Households"},
            {"key": "B", "text": "Census Villages (or Panchayat Wards)"},
            {"key": "C", "text": "Districts (Administrative boundaries)"},
            {"key": "D", "text": "Agricultural parcels of land"}
        ],
        "correct_option": "B",
        "explanation": "In large-scale rural sample surveys in India (such as NSS / PLFS), census villages (or sub-units in large villages) are selected as First Stage Units (FSUs), followed by households as Ultimate Stage Units (USUs)."
    },
    {
        "id": 2,
        "competency_code": "STAT_NAT_ACC",
        "competency_name": "National Accounts Statistics & Macro Aggregates",
        "domain": "Macroeconomic Statistics",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "According to the SNA 2008 framework adopted by MoSPI, what is the exact relationship between Gross Value Added (GVA) at Basic Prices and Gross Domestic Product (GDP) at Market Prices?",
        "options": [
            {"key": "A", "text": "GDP at Market Prices = GVA at Basic Prices + Product Taxes - Product Subsidies"},
            {"key": "B", "text": "GDP at Market Prices = GVA at Basic Prices - Production Taxes + Production Subsidies"},
            {"key": "C", "text": "GDP at Market Prices = GVA at Factor Cost + Direct Taxes"},
            {"key": "D", "text": "GDP at Market Prices = GVA at Basic Prices + Net Factor Income from Abroad"}
        ],
        "correct_option": "A",
        "explanation": "Under the current National Accounts series (Base 2011-12 onwards aligned with SNA 2008), GDP at Market Prices is derived by adding Product Taxes and subtracting Product Subsidies from GVA at Basic Prices."
    },
    {
        "id": 3,
        "competency_code": "STAT_COMPUTE",
        "competency_name": "Statistical Computing & Data Science",
        "domain": "Computing & Informatics",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "When analyzing microdata survey weights (multiplier) in Python using pandas to compute estimated population totals, which operation is methodologically correct?",
        "options": [
            {"key": "A", "text": "df['variable'].mean() directly on the unweighted sample"},
            {"key": "B", "text": "(df['variable'] * df['weight']).sum() / df['weight'].sum() for weighted mean, and (df['variable'] * df['weight']).sum() for total"},
            {"key": "C", "text": "df['variable'].sum() multiplied by total sample size"},
            {"key": "D", "text": "Standardizing the weights using z-score before calculating sum"}
        ],
        "correct_option": "B",
        "explanation": "In survey analysis with sampling multipliers/weights, the estimated population total is the sum of weighted values (value * weight), and the estimated weighted mean is the weighted sum divided by the sum of weights."
    },
    {
        "id": 4,
        "competency_code": "STAT_PRICE_IND",
        "competency_name": "Price Statistics & Index Numbers",
        "domain": "Price & Industrial Statistics",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "Which formula is predominantly utilized for the compilation of the all-India Consumer Price Index (CPI) and Index of Industrial Production (IIP) by MoSPI?",
        "options": [
            {"key": "A", "text": "Paasche's Current Weighted Formula"},
            {"key": "B", "text": "Fisher's Ideal Index Formula"},
            {"key": "C", "text": "Laspeyres Base Weighted Formula"},
            {"key": "D", "text": "Marshall-Edgeworth Formula"}
        ],
        "correct_option": "C",
        "explanation": "India's official CPI and IIP are compiled using the Laspeyres index formulation with fixed base year weights to ensure monthly comparability across commodity baskets."
    },
    {
        "id": 5,
        "competency_code": "STAT_LABOUR",
        "competency_name": "Labour & Demographic Statistics",
        "domain": "Socioeconomic Statistics",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "In the Periodic Labour Force Survey (PLFS), how is a person classified as 'Employed' under the Current Weekly Status (CWS) approach?",
        "options": [
            {"key": "A", "text": "Worked for at least 183 days during the preceding 365 days"},
            {"key": "B", "text": "Worked for at least 1 hour on any 1 day during the 7-day reference period"},
            {"key": "C", "text": "Worked for at least 8 hours every day during the reference month"},
            {"key": "D", "text": "Was actively seeking work throughout the preceding 30 days"}
        ],
        "correct_option": "B",
        "explanation": "Under the Current Weekly Status (CWS) methodology in PLFS, a person is considered employed if they performed economic activity for at least 1 hour on any one day during the 7-day reference period."
    },
    {
        "id": 6,
        "competency_code": "STAT_DATA_GOV",
        "competency_name": "Data Management & eSankhyiki Governance",
        "domain": "Data Governance",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "What is the primary function of the 'Macro Indicators Module' on the official MoSPI eSankhyiki portal?",
        "options": [
            {"key": "A", "text": "Downloading raw un-anonymized personal survey schedules"},
            {"key": "B", "text": "Providing programmatic API and interactive time-series access for core macroeconomic data (NAS, CPI, IIP, ASI)"},
            {"key": "C", "text": "Managing civil servant transfers and cadre postings"},
            {"key": "D", "text": "Hosting general public opinion polls"}
        ],
        "correct_option": "B",
        "explanation": "The Macro Indicators Module of eSankhyiki (esankhyiki.mospi.gov.in) provides filtered time-series data and official REST APIs for major statistical datasets including National Accounts, CPI, and IIP."
    },
    {
        "id": 7,
        "competency_code": "STAT_QUALITY",
        "competency_name": "Statistical Quality Assurance & Audit",
        "domain": "Quality & Standards",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "Which principle from the UN Fundamental Principles of Official Statistics emphasizes that official statistical agencies must maintain professional independence from political interference?",
        "options": [
            {"key": "A", "text": "Principle 1: Relevance, Impartiality, and Equal Access"},
            {"key": "B", "text": "Principle 2: Professional Standards and Ethics"},
            {"key": "C", "text": "Principle 5: Sources of Official Statistics"},
            {"key": "D", "text": "Principle 8: National Coordination"}
        ],
        "correct_option": "B",
        "explanation": "Principle 2 dictates that statistical agencies decide according to strictly professional considerations, scientific principles, and professional ethics on the methods and procedures for the collection and dissemination of data."
    },
    {
        "id": 8,
        "competency_code": "STAT_IND_AGRI",
        "competency_name": "Industrial & Enterprise Statistics",
        "domain": "Enterprise Statistics",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "In the Annual Survey of Industries (ASI), how is Net Value Added (NVA) computed from Gross Output and Total Inputs?",
        "options": [
            {"key": "A", "text": "NVA = Gross Output - Total Inputs - Depreciation"},
            {"key": "B", "text": "NVA = Gross Output + Rent + Interest"},
            {"key": "C", "text": "NVA = Total Inputs - Fuel Consumption"},
            {"key": "D", "text": "NVA = Gross Fixed Capital / Working Capital"}
        ],
        "correct_option": "A",
        "explanation": "In the Annual Survey of Industries (ASI), Net Value Added (NVA) is derived as Gross Output minus Total Inputs minus Depreciation."
    },
    {
        "id": 9,
        "competency_code": "STAT_VIZ_COMM",
        "competency_name": "Data Visualization & Official Communication",
        "domain": "Dissemination",
        "difficulty": "Intermediate",
        "is_common": True,
        "category": "common",
        "applicable_roles": ["all"],
        "question_text": "In the National Indicator Framework (NIF) for Sustainable Development Goals (SDGs) coordinated by MoSPI, what is the primary role of official interactive dashboards?",
        "options": [
            {"key": "A", "text": "To replace official gazette notifications completely"},
            {"key": "B", "text": "To enable transparent, interactive tracking of baseline targets and progress across States and Union Territories for policy makers"},
            {"key": "C", "text": "To store encrypted raw census files exclusively"},
            {"key": "D", "text": "To restrict public viewing of administrative metrics"}
        ],
        "correct_option": "B",
        "explanation": "MoSPI's SDG National Indicator Framework dashboard visualizes indicator progress across goals and states to support evidence-based policy making and public transparency."
    }
]

BASELINE_QUESTIONS = COMMON_CORE_QUESTIONS
DEPARTMENT_BASELINE_BANK["GENERAL"] = BASELINE_QUESTIONS

ROLE_SPECIFIC_QUESTION_BANK = {
    "senior": [
        {
            "id": 2001,
            "competency_code": "STAT_NAT_ACC",
            "competency_name": "National Accounts Statistics & Macro Aggregates",
            "domain": "Macroeconomic Statistics",
            "difficulty": "Advanced",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["senior", "director", "policy"],
            "question_text": "As a Senior Officer / Director analyzing SNA 2008 Supply and Use Tables (SUT) for macroeconomic policy, how are secondary product outputs balanced across institutional sectors?",
            "options": [
                {"key": "A", "text": "Reconciling product supply (output + imports) with product use (intermediate + final consumption + capital formation)"},
                {"key": "B", "text": "Excluding imports and exports from commodity flow accounting"},
                {"key": "C", "text": "Aggregating unverified micro-survey samples without price deflation"},
                {"key": "D", "text": "Fixing intermediate consumption ratios permanently without updating input structures"}
            ],
            "correct_option": "A",
            "explanation": "Supply and Use Tables (SUT) balance total commodity supply with total commodity use across all industries and institutional sectors under SNA 2008."
        },
        {
            "id": 2002,
            "competency_code": "STAT_QUALITY",
            "competency_name": "Statistical Quality Assurance & Audit",
            "domain": "Quality & Standards",
            "difficulty": "Advanced",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["senior", "director", "policy"],
            "question_text": "In executive quality governance under the UN National Quality Assurance Framework (NQAF), what is the primary policy requirement when releasing provisional GDP or CPI indicators?",
            "options": [
                {"key": "A", "text": "Publishing transparent revision schedules, methodological notes, and confidence indicators alongside provisional estimates"},
                {"key": "B", "text": "Withholding revision notes from public researchers permanently"},
                {"key": "C", "text": "Altering baseline figures retroactively without public documentation"},
                {"key": "D", "text": "Releasing data exclusively to registered commercial brokers"}
            ],
            "correct_option": "A",
            "explanation": "UN NQAF Principles mandate complete transparency regarding data revision policies, advance release calendars, and methodological documentation."
        },
        {
            "id": 2003,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Advanced",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["senior", "director", "policy"],
            "question_text": "For high-level inter-ministerial policy reporting on the Sustainable Development Goals (SDG India Index), how are raw indicator values normalized before goal score compilation?",
            "options": [
                {"key": "A", "text": "Rescaling raw indicators to a 0-100 target scale using official baseline and 2030 target benchmarks"},
                {"key": "B", "text": "Sorting states strictly by total land area"},
                {"key": "C", "text": "Assigning uniform 100 scores to all states regardless of empirical data"},
                {"key": "D", "text": "Using unverified online poll votes"}
            ],
            "correct_option": "A",
            "explanation": "NITI Aayog and MoSPI normalize SDG NIF indicators to a standard 0-100 distance-to-target scale to enable fair composite benchmarking across States/UTs."
        },
        {
            "id": 2004,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Advanced",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["senior", "director", "policy"],
            "question_text": "When senior statisticians design large-scale socio-economic sample surveys in SDRD, how is sample size allocated across states to ensure equal precision for sub-state domains?",
            "options": [
                {"key": "A", "text": "Applying Neyman allocation or proportional-to-size allocation with minimum sample caps per stratum"},
                {"key": "B", "text": "Allocating equal sample size to all villages regardless of population"},
                {"key": "C", "text": "Selecting households exclusively near capital cities"},
                {"key": "D", "text": "Eliminating stratification to simplify fieldwork"}
            ],
            "correct_option": "A",
            "explanation": "Optimum allocation (Neyman allocation) minimizes sampling variance for a given cost by allocating sample sizes proportional to stratum size and standard deviation."
        }
    ],
    "mid": [
        {
            "id": 3001,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Intermediate",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["mid", "sso", "officer"],
            "question_text": "For Mid-level Officers supervising NSS field operations, what is the mandatory protocol for handling non-response and casualty households in sample blocks?",
            "options": [
                {"key": "A", "text": "Replacing non-response units from casualty lists using prescribed systematic substitution rules and adjusting weights"},
                {"key": "B", "text": "Entering random fake numbers for non-responsive households"},
                {"key": "C", "text": "Canceling the entire sample block survey"},
                {"key": "D", "text": "Doubling the values of adjacent households without logging"}
            ],
            "correct_option": "A",
            "explanation": "Supervisory guidelines specify structured substitution protocols from reserve casualty lists and weight adjustments to prevent non-response bias."
        },
        {
            "id": 3002,
            "competency_code": "STAT_PRICE_IND",
            "competency_name": "Price Statistics & Index Numbers",
            "domain": "Price & Industrial Statistics",
            "difficulty": "Intermediate",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["mid", "sso", "officer"],
            "question_text": "In monthly CPI compilation by ESD officers, what is the required method for imputing missing item price quotations in selected markets?",
            "options": [
                {"key": "A", "text": "Applying cell-mean price relative growth rates from responding quotations in the same item group"},
                {"key": "B", "text": "Setting missing price quotations to zero permanently"},
                {"key": "C", "text": "Doubling the base year price automatically"},
                {"key": "D", "text": "Dropping the commodity group from national CPI"}
            ],
            "correct_option": "A",
            "explanation": "ESD standard operating procedure imputes missing monthly price quotes using the average price movement of responding units in the same commodity group."
        },
        {
            "id": 3003,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Intermediate",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["mid", "sso", "officer"],
            "question_text": "In Annual Survey of Industries (ASI) processing, how are factory units partitioned between the Census Sector and the Sample Sector?",
            "options": [
                {"key": "A", "text": "Units with 100+ workers are in Census Sector (100% enumerated); smaller units are sample-surveyed"},
                {"key": "B", "text": "Units are categorized purely by geographical proximity to port cities"},
                {"key": "C", "text": "Factories are selected based on voluntary online registration"},
                {"key": "D", "text": "All registered factories are surveyed every 10 years only"}
            ],
            "correct_option": "A",
            "explanation": "ASI frame partitions registered factories into Census Sector (large factories surveyed completely) and Sample Sector (statistically sampled)."
        },
        {
            "id": 3004,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Intermediate",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["mid", "sso", "officer"],
            "question_text": "During PLFS schedule supervision, how is an individual's Subsidiary Economic Activity Status (SS) distinguished from Usual Principal Status (UPS)?",
            "options": [
                {"key": "A", "text": "UPS measures major time spent (>= 183 days) in 365 days; SS captures secondary economic activity of >= 30 days"},
                {"key": "B", "text": "UPS is daily status; SS is annual status"},
                {"key": "C", "text": "UPS applies only to government civil servants"},
                {"key": "D", "text": "UPS measures pension eligibility; SS measures agricultural land size"}
            ],
            "correct_option": "A",
            "explanation": "UPS captures the principal activity pursued for the majority of the reference year (>= 183 days); SS captures secondary economic work of at least 30 days."
        }
    ],
    "junior": [
        {
            "id": 4001,
            "competency_code": "STAT_SURVEY",
            "competency_name": "Survey Methodology & Sampling Design",
            "domain": "Survey Operations",
            "difficulty": "Foundational",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["junior", "jso", "investigator"],
            "question_text": "During field canvassing by Statistical Investigators in FOD, what serves as the First Stage Unit (FSU) in rural sample blocks?",
            "options": [
                {"key": "A", "text": "Census Villages (or sub-units in large villages)"},
                {"key": "B", "text": "Individual households"},
                {"key": "C", "text": "Gram Panchayat Chairpersons"},
                {"key": "D", "text": "District Collectorate offices"}
            ],
            "correct_option": "A",
            "explanation": "In rural NSS surveys, Census Villages serve as First Stage Units (FSUs), within which sample households (USUs) are listed and selected."
        },
        {
            "id": 4002,
            "competency_code": "STAT_LABOUR",
            "competency_name": "Labour & Demographic Statistics",
            "domain": "Socioeconomic Statistics",
            "difficulty": "Foundational",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["junior", "jso", "investigator"],
            "question_text": "When conducting PLFS household interviews, how should an investigator record work activity under Current Weekly Status (CWS)?",
            "options": [
                {"key": "A", "text": "Classify as employed if the person worked for at least 1 hour on any 1 day during the 7-day reference period"},
                {"key": "B", "text": "Require continuous 8-hour work for all 7 days"},
                {"key": "C", "text": "Record work status based on monthly tax filings"},
                {"key": "D", "text": "Ignore part-time or casual wage work"}
            ],
            "correct_option": "A",
            "explanation": "Under CWS guidelines, performing economic activity for at least 1 hour on any day during the 7-day reference period qualifies as employed."
        },
        {
            "id": 4003,
            "competency_code": "STAT_IND_AGRI",
            "competency_name": "Industrial & Enterprise Statistics",
            "domain": "Enterprise Statistics",
            "difficulty": "Foundational",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["junior", "jso", "investigator"],
            "question_text": "During ASI field visits to registered factories, which physical financial document must be verified by field investigators?",
            "options": [
                {"key": "A", "text": "Audited balance sheet, profit & loss statement, and attendance/payroll registers"},
                {"key": "B", "text": "Worker personal utility bills only"},
                {"key": "C", "text": "Unverified verbal statements from gate guards"},
                {"key": "D", "text": "Factory owner personal residential tax returns"}
            ],
            "correct_option": "A",
            "explanation": "ASI field verification requires auditing books of accounts, audited financial statements, and output/labor registers from factory records."
        },
        {
            "id": 4004,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Foundational",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["junior", "jso", "investigator"],
            "question_text": "How do CAPI (Computer Assisted Personal Interviewing) handheld tablets improve field data entry quality for investigators?",
            "options": [
                {"key": "A", "text": "Built-in validation checks, logical consistency rules, geo-location tagging, and instant upload"},
                {"key": "B", "text": "Replacing household field visits completely"},
                {"key": "C", "text": "Preventing field supervisors from auditing survey schedules"},
                {"key": "D", "text": "Allowing investigators to fill schedules without visiting sample units"}
            ],
            "correct_option": "A",
            "explanation": "CAPI tablets incorporate real-time entry validation range checks and timestamping to enhance field data quality."
        }
    ],
    "technical": [
        {
            "id": 5001,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Advanced",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["technical", "analyst", "data_science"],
            "question_text": "In Python microdata processing pipelines, which pandas syntax correctly computes a weighted average across survey units using multiplier weights?",
            "options": [
                {"key": "A", "text": "(df['val'] * df['weight']).sum() / df['weight'].sum()"},
                {"key": "B", "text": "df['val'].mean() * df['weight'].mean()"},
                {"key": "C", "text": "df['val'].sum() / len(df)"},
                {"key": "D", "text": "df['val'].std() * df['weight'].sum()"}
            ],
            "correct_option": "A",
            "explanation": "Weighted mean calculation requires multiplying values by sampling weights, summing the product, and dividing by total sample weight."
        },
        {
            "id": 5002,
            "competency_code": "STAT_DATA_GOV",
            "competency_name": "Data Management & eSankhyiki Governance",
            "domain": "Data Governance",
            "difficulty": "Advanced",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["technical", "analyst", "data_science"],
            "question_text": "When preparing unit-record microdata for eSankhyiki open data portal dissemination, what anonymization technique protects respondent privacy?",
            "options": [
                {"key": "A", "text": "Suppressing direct identifiers, top-coding extreme financial values, and masking micro-geographic codes"},
                {"key": "B", "text": "Publishing full names, Aadhaar numbers, and phone numbers"},
                {"key": "C", "text": "Encrypting microdata files permanently without public keys"},
                {"key": "D", "text": "Removing sampling multiplier weights from microdata files"}
            ],
            "correct_option": "A",
            "explanation": "Statistical disclosure control standards require top-coding extreme values, masking geographic sub-districts, and suppressing direct identifiers."
        },
        {
            "id": 5003,
            "competency_code": "STAT_COMPUTE",
            "competency_name": "Statistical Computing & Data Science",
            "domain": "Computing & Informatics",
            "difficulty": "Intermediate",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["technical", "analyst", "data_science"],
            "question_text": "For large-scale MoSPI survey microdata ETL, how should memory-constrained batch data loading be handled in Python pandas?",
            "options": [
                {"key": "A", "text": "Processing data in chunks using pd.read_csv(..., chunksize=N) or using optimized parquet file storage"},
                {"key": "B", "text": "Loading entire raw datasets into Python list objects in a single unoptimized loop"},
                {"key": "C", "text": "Converting all numeric columns to raw string types"},
                {"key": "D", "text": "Deleting non-zero rows to reduce memory usage"}
            ],
            "correct_option": "A",
            "explanation": "Chunked processing (`chunksize`) and columnar formats (Parquet) enable efficient memory management for multi-gigabyte survey datasets."
        },
        {
            "id": 5004,
            "competency_code": "STAT_VIZ_COMM",
            "competency_name": "Data Visualization & Official Communication",
            "domain": "Dissemination",
            "difficulty": "Intermediate",
            "is_common": False,
            "category": "role_specific",
            "applicable_roles": ["technical", "analyst", "data_science"],
            "question_text": "What architecture is recommended for building automated RESTful data dissemination APIs for open statistical portals?",
            "options": [
                {"key": "A", "text": "FastAPI/Flask REST endpoints delivering JSON payloads with OpenAPI schema documentation and CORS security"},
                {"key": "B", "text": "Generating static HTML files sent manually via email attachments"},
                {"key": "C", "text": "Binary proprietary file downloads requiring physical USB dongles"},
                {"key": "D", "text": "Unencrypted raw database socket connections exposed to public internet"}
            ],
            "correct_option": "A",
            "explanation": "Modern open statistical dissemination portals utilize REST APIs with standardized JSON payloads and OpenAPI specifications."
        }
    ]
}
DEPARTMENT_BASELINE_BANK["GENERAL"] = BASELINE_QUESTIONS


RESOURCES_SEED = [
    {
        "title": "NSSTA Induction Module: Foundations of Official Statistics in India",
        "description": "Official academy curriculum covering the organizational structure of MoSPI, the Indian Statistical System, National Statistical Commission (NSC) guidelines, and administrative data flows.",
        "source": "NSSTA",
        "official_url": "https://www.mospi.gov.in/national-statistical-systems-training-academy-nssta",
        "resource_type": "Training_Module",
        "difficulty": "Foundational",
        "estimated_duration_mins": 180,
        "competency_code": "STAT_SURVEY"
    },
    {
        "title": "NSSTA Digital Data Lab: Data Analytics with Python for Statistical Officers",
        "description": "Applied laboratory course on microdata wrangling, descriptive statistics, automated data validation pipelines, and visual reporting using Python pandas, numpy, and matplotlib.",
        "source": "NSSTA",
        "official_url": "https://www.mospi.gov.in/national-statistical-systems-training-academy-nssta",
        "resource_type": "Training_Module",
        "difficulty": "Intermediate",
        "estimated_duration_mins": 240,
        "competency_code": "STAT_COMPUTE"
    },
    {
        "title": "MoSPI NAD: National Accounts Statistics (SNA 2008) Framework & Estimation",
        "description": "Official National Accounts Division training manual on GDP/GVA estimation methodologies, sequence of accounts, Supply and Use Tables (SUT), and capital asset measurement.",
        "source": "MoSPI",
        "official_url": "https://www.mospi.gov.in/national-accounts-division-nad",
        "resource_type": "Publication",
        "difficulty": "Advanced",
        "estimated_duration_mins": 300,
        "competency_code": "STAT_NAT_ACC"
    },
    {
        "title": "NSSTA Advanced Curriculum: Survey Sampling & Multi-Stage Design",
        "description": "Official academy curriculum on stratified multistage sampling, allocation of sample sizes across strata, circular systematic sampling, and variance estimation in household surveys.",
        "source": "NSSTA",
        "official_url": "https://www.mospi.gov.in/survey-design-and-research-division-sdrd",
        "resource_type": "Training_Module",
        "difficulty": "Advanced",
        "estimated_duration_mins": 210,
        "competency_code": "STAT_SURVEY"
    },
    {
        "title": "NSSTA Digital Data Lab: Microdata Processing & Anonymization Standards",
        "description": "Hands-on laboratory manual on statistical disclosure control (SDC), k-anonymity, top-coding, and noise addition for open statistical datasets on eSankhyiki.",
        "source": "NSSTA",
        "official_url": "https://esankhyiki.mospi.gov.in/",
        "resource_type": "Training_Module",
        "difficulty": "Intermediate",
        "estimated_duration_mins": 150,
        "competency_code": "STAT_DATA_GOV"
    },
    {
        "title": "MoSPI ESD: Consumer Price Index (CPI) & IIP Compilation Handbook",
        "description": "Standard operating procedures for price quote validation, geometric mean aggregation at item level, and chained Laspeyres index number calculations.",
        "source": "MoSPI",
        "official_url": "https://www.mospi.gov.in/economic-statistics-division-esd",
        "resource_type": "Publication",
        "difficulty": "Intermediate",
        "estimated_duration_mins": 120,
        "competency_code": "STAT_PRICE_IND"
    },
    {
        "title": "MoSPI eSankhyiki Portal: Data Catalogue & Macro Indicators Guide",
        "description": "Official documentation for accessing core data products on eSankhyiki, utilizing REST endpoints, and integrating national data with state directorates.",
        "source": "MoSPI",
        "official_url": "https://esankhyiki.mospi.gov.in/",
        "resource_type": "Dataset",
        "difficulty": "Intermediate",
        "estimated_duration_mins": 90,
        "competency_code": "STAT_DATA_GOV"
    },
    {
        "title": "MoSPI Periodic Labour Force Survey (PLFS) Annual Report & Methodology",
        "description": "Official technical report detailing sampling design, rotation scheme, activity definitions, UPSS vs CWS estimation formulas, and key labour indicators.",
        "source": "MoSPI",
        "official_url": "https://www.mospi.gov.in/publication/all-india-annual-report-plfs",
        "resource_type": "Publication",
        "difficulty": "Intermediate",
        "estimated_duration_mins": 180,
        "competency_code": "STAT_LABOUR"
    },
    {
        "title": "MoSPI Annual Survey of Industries (ASI) Concepts & Operational Manual",
        "description": "Comprehensive reference handbook for industrial classification (NIC-2008), frame maintenance, schedule canvassing, and value added estimation.",
        "source": "MoSPI",
        "official_url": "https://www.mospi.gov.in/annual-survey-industries",
        "resource_type": "Publication",
        "difficulty": "Foundational",
        "estimated_duration_mins": 140,
        "competency_code": "STAT_IND_AGRI"
    },
    {
        "title": "MoSPI Sustainable Development Goals (SDG) National Indicator Report",
        "description": "Guidelines on metadata construction, baseline-to-target tracking, data visualization dashboards, and state progress comparison reports.",
        "source": "MoSPI",
        "official_url": "https://www.mospi.gov.in/sustainable-development-goals-sdg",
        "resource_type": "Publication",
        "difficulty": "Intermediate",
        "estimated_duration_mins": 130,
        "competency_code": "STAT_VIZ_COMM"
    },
    {
        "title": "NSSTA Quality Assurance & Audit Handbook for Official Statistics",
        "description": "Practical implementation of UN NQAF standards, data validation checklists, non-sampling error auditing, and field supervision manuals.",
        "source": "NSSTA",
        "official_url": "https://www.mospi.gov.in/national-statistical-systems-training-academy-nssta",
        "resource_type": "Training_Module",
        "difficulty": "Advanced",
        "estimated_duration_mins": 160,
        "competency_code": "STAT_QUALITY"
    }
]
