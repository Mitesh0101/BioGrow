# BioGrow
**Smart Agricultural Ecosystem & Community Platform**

## 1. Executive Summary
BioGrow is a web-based integrated agricultural platform designed to empower farmers with data-driven decision-making tools and a robust support community. By leveraging Machine Learning for crop prediction, Generative AI for real-time assistance, and gamification for peer-to-peer problem solving, BioGrow addresses the technological gap in modern farming. The platform serves as a "digital companion" for farmers, providing end-to-end support from soil analysis to harvest, while fostering a collaborative ecosystem.

## 2. Problem Statement
Despite agriculture being a primary economic sector, farmers often suffer from low yields and economic loss due to:
* **Lack of Scientific Planning:** Inability to choose the optimal crop based on specific soil parameters (N, P, K, pH) and climatic conditions.
* **Information Asymmetry:** Limited access to real-time solutions for crop diseases and pest infestations.
* **Weather Unpredictability:** Lack of timely, actionable alerts regarding severe weather events.
* **Isolation:** Absence of a dedicated platform to discuss issues, share knowledge, and collaborate with other farmers.

## 3. Proposed Solution
BioGrow provides a holistic solution by combining three core pillars:
* **AI/ML Advisory:** A Machine Learning model to recommend the most viable crops based on user-provided soil lab reports, supplemented by an AI Chatbot for instant queries.
* **Community-Led Support:** A "Stack Overflow-style" forum where farmers raise issues and experts/peers provide solutions. This is driven by a gamified economy where helpful contributions earn points.
* **Proactive Alerts:** A weather monitoring system that pushes critical alerts via email to prevent crop damage.

## 4. Target Audience
* **Primary Users:** Farmers and Agricultural Enthusiasts who seek scientific guidance for crop planning.
* **Secondary Users:** Agricultural Experts and Students who wish to contribute knowledge and earn community recognition.
* **Administrators:** System managers responsible for platform maintenance and moderation.

## 5. Technology Stack
* **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5 (Responsive/Mobile-First Design).
* **Backend:** Python (Flask Framework).
* **Database:** PostgreSQL (Relational Database for Users, Issues, and Transactions).
* **Machine Learning:** Scikit-Learn (Decision Tree/Random Forest for Crop Prediction).
* **AI Integration:** Google Gemini API (Chatbot & Solution Validation).
* **APIs & Services:** OpenWeatherMap API (Real-time Weather Data), SendGrid (Email Notifications), Web Speech API (Voice-to-Text Input).

## 6. Functional Modules & Features

### 6.1. Smart Crop & Fertilizer Recommendation
* **Input:** Users enter soil test values (Nitrogen, Phosphorous, Potassium, Soil pH, Temperature, Relative Humidity and Soil Type).
* **Processing:** The backend utilizes a pre-trained Machine Learning model to analyze inputs.
* **Output:** Recommends the optimal crop to cultivate and generates a downloadable PDF report detailing fertilizer schedules.

### 6.2. Gamified Community Forum
* **Raise Issue:** Farmers can post queries with images (e.g., diseased leaves) and descriptions.
* **Voice Support:** Integrated Voice-to-Text feature allows users to dictate issues instead of typing.
* **Solution System:** Peers can comment solutions. The Original Poster (OP) marks the best solution.
* **AI Validation (Safety Net):** Before points are awarded, the "Best Solution" is cross-referenced by the Gemini API to ensure safety and relevance.



#### 6.2.1 Create New Topic (Posting an Issue)

Farmers can raise a new issue by submitting relevant details about their problem.
 
**User Inputs:**
- Title  
- Description  

**How It Works:**
- **Text Input:**  
  When the user clicks **Submit**, the title and description are saved in the database.
- **Voice Input:**  
  When the microphone button is clicked, the browser listens to the user’s voice, converts speech into text using the Web Speech API, and automatically fills the input fields.
- **Image Upload:**  
  If the user uploads an image (e.g., a diseased leaf):
  - The actual image file is stored on the server.
  - The image file path/link is saved in the database and associated with the topic.


#### 6.2.2 Topic Feed (Main Topic List)

This is the primary interface displaying all recently raised issues.

**Concept:**
- A scrollable list of topic cards.
- Each card displays a short summary of the issue.

**How It Works:**
- Pinned (important) topics are displayed at the top.
- Remaining topics are sorted by most recent first.
- Only 10 topics are loaded per request to prevent performance issues.
- A **“Next Page”** button allows loading additional topics.


#### 6.2.3 Priority Pinning (Gamification Feature)

Allows users to use earned points to highlight urgent issues.

**Concept:**
- A **“Pay with Points”** option that pins a topic to the top of the feed.

**How It Works:**
- The system checks the user’s point balance.
- If sufficient points are available:
  - Points are deducted.
  - The topic is marked as **Pinned** for 24 hours.
- If points are insufficient:
  - An error message **“Insufficient funds”** is displayed.


#### 6.2.4 Smart Suggestion Feature (Duplicate Issue Prevention)

Helps users find existing solutions while typing a new issue.

**How It Works:**
- As the user types the issue title, a JavaScript event listener captures the text.
- The frontend sends the text to the backend via an AJAX request.
- The backend searches previously solved topics for similar keywords.
- Matching results are displayed as clickable suggestions, for example:  
  **[SOLVED] White fungus on potato leaves**
- The user can open the suggested solution and avoid creating a duplicate topic.


#### 6.2.5 Search and Category Filtering

Improves discoverability of forum topics.

**Concept:**
- Category filters such as **Pests**, **Soil**, and **Weather**.

**How It Works:**
- **Search Bar:**  
  The system searches titles and descriptions for matching keywords entered by the user.
- **Category Filter:**  
  Selecting a category displays only topics tagged under that category.


#### 6.2.6 Edit & Delete Topics

Allows users to manage their own forum posts.

**Concept:**
- Users can edit mistakes or remove their topics.

**How It Works:**
- Before allowing edit or delete actions:
  - The system compares the **Logged-in User ID** with the **Topic Author ID**.
- If both match, the action is allowed.
- If they do not match, the action is blocked.


### 6.3. The Economy of Points (Gamification)
* **Earning:** Users earn points by having their answers marked as "Solutions" or by daily check-ins.
* **Spending (Redemption):** Points can be redeemed for premium digital features:
    * **Priority Pin:** Pin an urgent issue to the top of the feed for 24 hours.
    * **Expert Badge:** Visual distinction ("Golden Turban") on the user profile.
    * **Ad-Free Mode:** Simulation of a premium, distraction-free interface.

### 6.4. AI Assistant (Chatbot)
A dedicated floating chatbot powered by Gemini API to answer general agricultural queries instantly (e.g., "What is the market price of wheat?", "How to treat aphids?").

### 6.5. Weather & Alerts
* **Real-time dashboard:** Showing temperature, humidity, and forecast.
* **Critical Alerts:** Automated email notifications sent to users via SendGrid when severe weather conditions (e.g., heavy rain, frost) are predicted for their registered location.

### 6.6. Integrated Crop Tracking & Monitoring System
To address the lack of expensive IoT infrastructure in small-scale farming, BioGrow incorporates a "Manual Observation Framework." This module allows farmers to input low-cost, high-impact field data, which the system compares against standard agronomical benchmarks to generate health alerts.

#### 6.6.1. Vegetative Growth Tracking (Plant Height)
* **Methodology:** Users input the vertical growth of the plant (in cm) on a weekly basis.
* **Significance:** The system compares current height against the crop’s standard growth curve to identify stunted growth phases caused by nutrient or water stress.

#### 6.6.2. Nitrogen Analysis via Leaf Color Chart (LCC)
* **Methodology:** Users compare the crop’s leaf color against a standardized 6-point green scale (1=Yellowish-Green, 6=Dark Green).
* **Significance:** Acts as a cost-effective alternative to chlorophyll meters, triggering precise urea/nitrogen application recommendations when values drop below the crop-specific threshold.

#### 6.6.3. Qualitative Soil Moisture Assessment
* **Methodology:** Users perform a "hand-feel" test and select the soil status from a predefined set (Dry/Loose, Moist/Ball, Wet/Sticky).
* **Significance:** Substitutes digital moisture sensors to provide immediate irrigation alerts, preventing both wilt (under-watering) and root rot (over-watering).

#### 6.6.4. Visual Pest Intensity Scoring
* **Methodology:** A standardized visual inspection of 5 random plants, rated on a damage scale of 0 (No Damage) to 4 (Severe Infestation >50%).
* **Significance:** Moves beyond binary "yes/no" reporting to track infestation severity, allowing the system to recommend pesticide intervention only when economic threshold levels are breached.

#### 6.6.5. Weed Pressure Quantification
* **Methodology:** Users estimate the percentage of ground cover occupied by weeds within a 1x1 meter sample area.
* **Significance:** Identifies nutrient competition. High weed pressure triggers a "Weeding Alert" and temporarily pauses fertilizer recommendations to prevent feeding the weeds.

#### 6.6.6. Stand Count & Population Density
* **Methodology:** A count of viable plants within a standardized 1x1 meter frame, taken at the seedling stage.
* **Significance:** Detects germination failure or early-stage pest damage, allowing the system to recalibrate yield predictions based on actual plant population rather than theoretical capacity.

#### 6.6.7. Phenological Stage Logging
* **Methodology:** Users record the specific dates of biological milestones (e.g., "Date of First Flower," "Date of Fruit Set").
* **Significance:** Tracks the crop’s biological clock against the calendar. Delays in phenology trigger alerts regarding potential heat stress or delayed harvest windows.

#### 6.6.8. Yield Estimation (Fruit/Pod Count)
* **Methodology:** An average count of fruits or pods per plant, taken from a random sample of 5 plants during the reproductive stage.
* **Significance:** Provides the primary variable for the Machine Learning yield prediction model, refining the harvest volume estimate (Yield = Plant Density × Avg. Fruit Count).

#### 6.6.9. Root Health Diagnostics
* **Methodology:** A monthly visual check of the root system (via digging up a single sample plant) to categorize root color (White/Cream vs. Brown/Black).
* **Significance:** Enables early detection of soil-borne fungal pathogens (e.g., Root Rot) that are not immediately visible on the foliage.

#### 6.6.10. Canopy Coverage Efficiency
* **Methodology:** A visual estimation of shadow coverage on the soil (Open, Partial, or Closed Canopy) at solar noon.
* **Significance:** Indicates photosynthetic efficiency and biomass production. Failure to achieve "Closed Canopy" by a specific week signals underlying agronomic issues.

## 7. Future Scope
* **Computer Vision Integration:** "Leaf Doctor" feature to detect diseases automatically by scanning uploaded images using Convolutional Neural Networks (CNN).
* **Marketplace Integration:** Real-time "Mandi" (Market) prices for crops in different districts.
* **Multilingual Support:** Localization of the UI into regional languages for better accessibility.

## 8. Algorithmic Implementation Rules
To automate the decision-making process for the "Manual Observation Framework" (Section 6.6), the following logic gates and threshold comparisons are implemented within the Flask backend.

### 8.1. Vegetative Growth Analysis (Height)
* **Input:** `Current_Height_CM`, `Week_Number`
* **Logic:** The system retrieves the `Standard_Height` for the specific crop and week from the knowledge base.
    * **Rule 1 (Stunting):** If `Current_Height < (0.70 × Standard_Height)`, trigger **"Stunted Growth Alert"**.
    * **Rule 2 (Etiolation):** If `Current_Height > (1.30 × Standard_Height)`, trigger **"Etiolation/Low-Light Warning"**.

### 8.2. Nitrogen Quantification (LCC)
* **Input:** `LCC_Score` (1-6)
* **Logic:** Compare against crop-specific `Optimal_LCC` (e.g., Rice=4).
    * **Rule 1 (Deficiency):** If `LCC_Score < Optimal_LCC`:
        * Calculate `Deficit = Optimal_LCC - LCC_Score`.
        * **Recommendation:** `"Apply Nitrogen: " + (Deficit × 15) + " kg Urea/acre"`.
    * **Rule 2 (Toxicity):** If `LCC_Score > 5`, trigger **"Nitrogen Toxicity Alert"** (Cease fertilization to prevent pest susceptibility).

### 8.3. Soil Moisture Logic
* **Input:** `Soil_Feel` (Mapped: Dry=1, Moist=2, Wet=3)
* **Logic:** Compare against `Required_Moisture` for the current phenological stage.
    * **Rule 1 (Water Stress):** If `Soil_Feel < Required_Moisture`, trigger **"Critical Irrigation Alert"**.
    * **Rule 2 (Rot Risk):** If `Soil_Feel > Required_Moisture AND Stage == "Ripening"`, trigger **"Fungal Rot Risk"**.

### 8.4. Pest Intervention Thresholds
* **Input:** `Pest_Severity_Score` (0-4)
* **Logic:**
    * **Score 1:** Recommend **"Biological Control"** (e.g., Neem Oil, Pheromone Traps).
    * **Score 2-3:** Recommend **"Chemical Control"** (Crop-specific pesticide application).
    * **Score 4:** Recommend **"Crop Isolation/Destruction"** to prevent field-wide contagion.

### 8.5. Weed Competition Lock
* **Input:** `Weed_Coverage_Percent`
* **Logic:**
    * **Rule:** If `Weed_Coverage_Percent > 30%`:
        * **Action:** System locks the "Fertilizer Recommendation" module.
        * **Alert:** "Fertilizer recommendations paused. High weed pressure detected; application now will primarily feed weeds. Please de-weed first."

### 8.6. Stand Count & Resowing Logic
* **Input:** `Actual_Plants_Per_M2`
* **Logic:** Calculate `Survival_Rate = Actual_Plants / Expected_Density`.
    * **Rule:** If `Survival_Rate < 0.40 (40%)`:
        * **Recommendation:** "Critical Germination Failure. Economic threshold for viability not met. Recommend immediate resowing."

### 8.7. Phenological Timing Check
* **Input:** `Event_Date`, `Planting_Date`
* **Logic:** Calculate `Days_Elapsed = Event_Date - Planting_Date`.
    * **Rule 1 (Heat Stress):** If `Days_Elapsed < Min_Expected_Days` (e.g., Flowering at Day 40 instead of 60), trigger **"Early Bolting/Heat Stress Alert"**.
    * **Rule 2 (Photoperiod Delay):** If `Days_Elapsed > Max_Expected_Days`, trigger **"Delayed Growth Alert"**.

### 8.8. Yield Prediction Formula
* **Input:** `Avg_Fruits_Per_Plant`, `Stand_Count`
* **Logic:**
    * `Total_Fruits_Per_Acre = Avg_Fruits_Per_Plant × (Stand_Count × 4046 m²)`
    * `Predicted_Yield_Kg = (Total_Fruits × Avg_Fruit_Weight_Grams) / 1000`
* **Output:** Updates the user's "Expected Revenue" dashboard.

### 8.9. Root Health Diagnostics
* **Input:** `Root_Color` (Enum)
* **Logic:**
    * **Input "Brown":** Trigger **"Water Stress Warning"** (Suberization of roots).
    * **Input "Black/Mushy":** Trigger **"CRITICAL: Root Rot Alert"**. Recommend immediate drainage and fungicide drench.

### 8.10. Canopy Efficiency Check
* **Input:** `Canopy_Status` (Open/Partial/Closed), `Week_Number`
* **Logic:**
    * **Rule 1:** If `Week_Number > 8 AND Canopy_Status == "Open"`:
        * Trigger **"Low Biomass Alert"** (Yield potential significantly reduced).
    * **Rule 2:** If `Week_Number < 4 AND Canopy_Status == "Closed"`:

        * Trigger **"Overcrowding Alert"** (High risk of microclimate-induced fungal disease).
