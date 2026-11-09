# Global-Catholic-Liturgy-API-Bot
API integration and scheduling pipeline that checks live stream status and rotates between Western and Eastern Catholic rites
## Project Overview
Developed a Python-based automation system for a large Discord community to schedule, validate, and stream global Catholic liturgies. The system alternated weekly between Western (Latin) rites and various Eastern Catholic rites (e.g., Syro-Malabar, Byzantine) to provide a diverse liturgical experience.

## The Problem
The community moderator was manually checking YouTube links every Sunday to see if a specific church was actively streaming their Mass. This was inefficient, error-prone, and resulted in dead links. Additionally, the schedule needed to ensure variety, rotating between different Eastern Catholic rites without repeating until the full list was exhausted.

## Technical Stack
*   **Language:** Python
*   **Libraries:** Requests (API integration), Pandas (Data structuring)
*   **Integrations:** YouTube APIs, Google Cloud Services
*   **Output:** Google Sheets (for schedule tracking and community visibility)

## Methodology & Features
1.  **Weekly Rite Rotation:** Built a logical randomizer/scheduler that alternated between Western rites and a list of Eastern Catholic rites, enforcing a "no-repeat" rule until the cycle was complete.
2.  **Live API Validation:** The Python script integrated with YouTube APIs to ping the data endpoints and verify if a stream was currently live for the scheduled church. This eliminated the need for manual link checking.
3.  **Cloud Infrastructure Setup:** Configured Google Cloud APIs, including navigating the OAuth consent screen and API publishing/verification process to ensure the application could run seamlessly and reliably.
4.  **Data Logging:** Utilized Pandas and Google Sheets API to log the schedule and API responses.

## Challenges & Learnings (The Consultant Insights)
*   **Data Source Unreliability:** Discovered that not all church streamers adhere to a strict schedule or maintain high-quality streams. The system had to be built to handle missing data or offline channels without crashing.
*   **Cloud Infrastructure:** Learned the intricacies of Google Cloud API publishing, authentication, rate limits, and token refreshing.
*   **ROI Assessment:** Ultimately, the project was a successful proof-of-concept. After building it, I determined that for a single user, checking a schedule manually was faster than maintaining the script. I successfully proved the concept, learned API integration, and retired the project to focus on higher-yield data pipelines.

## Business Value
*   Proves capability in connecting to third-party APIs (YouTube, Google Cloud).
*   Demonstrates the ability to build automated data validation pipelines.
*   Shows pragmatic decision-making (knowing when a tool is over-engineered for the specific use case).
