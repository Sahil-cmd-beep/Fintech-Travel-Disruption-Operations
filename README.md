# High-Volume Fintech & Travel Disruption Operations Pipeline

## 📌 Project Overview
This repository constructs a production-simulated data environment that mimics how high-volume travel integrations (flights, cancellations, PNR recovery workflows) intersect with digital neobank backend architecture (multi-currency handling, user tier prioritizing, automated clearing house failures).

The objective is to establish an automated analytical framework that detects operational breakdown anomalies, calculates customer experience infrastructure strain (SLA breaches, AHT extensions), and designs a data-backed fallback solution to triage premium users during massive external vendor failures (e.g., global airline cancellations).

## 🗂 Data Schema Design
The project models production systems via four key structural entities:
*   `users`: Tracks subscription tiers (`Standard` to `Ultra`) to determine service priority tiers.
*   `transactions`: Monitored processing outcomes including multi-currency conversions and refund logic flags (`completed`, `failed`, `refunded`).
*   `flight_bookings`: Feeds travel telemetry (PNR, ticket status, operating airline validation) into system logic.
*   `support_tickets`: Logs operational system strains via structural queue handle times.

## 🛠 Strategic Action & Insights Derived
Through the simulated anomaly logic included in `data_generation.py`, a simulated structural flight disruption caused automated international refund pipelines to face cross-border settlement timeouts. 

### Data-Driven Solutions Implemented:
1. **Premium Tier Prioritization:** Using analytic window calculations (`operational_analytics.sql`), the system isolates and flags `Ultra` and `Metal` users with trapped transaction capital, shifting them out of the standard chat queue and into dedicated high-priority recovery flows.
2. **Defensive Batch Queuing:** To lower the 40% transaction failure spike observed during systemic vendor API drop-offs, the structural analysis proposes a delayed processing pipeline that batches cross-currency adjustments instead of instantly dropping the request.

## 🚀 How to Run the Environment
1. Clone the repository to your environment.
2. Generate the SQLite relational baseline by executing the data engine:
   ```bash
   python data_generation.py
   ```
3. Run the analytical queries inside `operational_analytics.sql` using any SQL engine or DB browser to inspect data logs.
