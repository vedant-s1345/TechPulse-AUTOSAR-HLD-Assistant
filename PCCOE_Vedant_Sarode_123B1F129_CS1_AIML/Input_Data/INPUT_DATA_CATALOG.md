# Input Data & Synthetic Knowledge Base Catalog
**TechPulse FY-26 Applied AI/ML Capstone — Case Study 1 (CS1)**  
**Document Classification:** Synthetic Engineering Demonstration Data  

---

> [!IMPORTANT]
> **SYNTHETIC DATA DISCLAIMER:**  
> All files in this folder are **synthetic engineering references** created specifically for the academic evaluation of the TechPulse FY-26 Capstone Project. They **do NOT contain proprietary OEM specifications**, trade secrets, or certified production AUTOSAR/ISO 26262 artifacts. They are designed to mirror realistic automotive software architecture documents to rigorously test ingestion, chunking, retrieval, and grounding capabilities.

---

## 1. Document Inventory

| Document Filename | Format | Pages | System Domain | Key Architectural Entities | Purpose in Evaluation |
|---|---|---|---|---|---|
| `SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf` | Digital PDF | 3 | High-Voltage Battery Management System (BMS) | `BmsCellSupervisor_SWC`, `BmsThermalControl_SWC`, `BmsSocEstimator_SWC`, `If_CellVoltageArray`, Sequence `FF-BMS-01`, ASIL C / ASIL D | Tests direct factual retrieval, interface identification, multi-SWC coordination, and functional flow sequence timing. |
| `SYNTHETIC_AUTOSAR_Brake_By_Wire_HLD.pdf` | Digital PDF | 3 | Electronic Brake-by-Wire (BBW) Subsystem | `PedalSensorReader_SWC`, `BrakeDecelArbitrator_SWC`, `WheelBrakeActuator_SWC`, `If_PedalTravel`, Sequence `FF-BBW-02`, ASIL D | Tests safety ASIL allocation retrieval, sensor plausibility voting, emergency braking sequences, and fail-silent constraints. |
| `SYNTHETIC_AUTOSAR_ADAS_Fusion_HLD.pdf` | Digital PDF | 3 | ADAS Camera & Radar Perception Fusion (L2+) | `FrontCameraTracker_SWC`, `RadarClusterProcessor_SWC`, `ObjectFusionArbitrator_SWC`, `SOME/IP` Event `VisionObjectTracks`, Sequence `FF-ADAS-03` | Tests SOME/IP Ethernet interface identification, Time-to-Collision (TTC) calculations, and graceful degradation under sensor occlusion. |
| `SYNTHETIC_SCANNED_DUMMY_OCR_REQUIRED.pdf` | Vector/Image PDF | 1 | Non-Extractable Diagram Dummy | Blank text layer with vector bounding boxes | Tests the ingestion engine's capability to detect scanned pages and issue clear OCR error warnings. |
| `SYNTHETIC_CORRUPTED_FILE.pdf` | Malformed Binary | 1 | Deliberately Damaged Stream | Truncated PDF header | Tests exception handling and resilience against corrupted document uploads. |

---

## 2. In-Depth Architectural Summaries

### A. Powertrain Battery Management System HLD (`SYNTHETIC_AUTOSAR_Powertrain_BMS_HLD.pdf`)
- **Page 1: Document Control & High-Level System Context:**
  - Revision 2.1; 800V lithium-ion battery pack supervisory controller running on AUTOSAR Classic 4.4.0 RTE.
  - Subsystems: Cell Supervisor (10ms, ASIL C), Thermal Control (100ms, ASIL B), Contactor Manager (5ms CDD, ASIL D), State Estimator (20ms, ASIL C).
- **Page 2: Software Component & Port Catalog:**
  - `BmsCellSupervisor_SWC`: Over-voltage threshold (4.25V), under-voltage threshold (2.70V). ReceiverPort `RPort_CellVoltage` with Sender-Receiver interface `If_CellVoltageArray` (192 channels). ProvidePort `PPort_CellAlert` (Client-Server `If_CellFaultNotification`).
  - `BmsThermalControl_SWC`: ReceiverPort `RPort_PackTemp`, ProvidePort `PPort_PumpCmd` (PWM 0-100%).
  - `BmsSocEstimator_SWC`: Extended Kalman Filter (EKF), sampling current at 1 kHz (`If_PackCurrent`), estimating SOC float32 (`If_StateOfCharge`).
- **Page 3: Functional Sequences & Safety Goals:**
  - Sequence `FF-BMS-01`: Over-Voltage Protection Flow (detects cell > 4.28V for >3 cycles -> asserts `PPort_CellAlert` -> `BmsContactorManager_CDD` opens pyrofuse within 20ms -> DTC `0x1A094F` logged).
  - Safety Goal `SG-01`: Fault Handling Time Interval (FHTI) = 50 ms. CAN-FD latency <= 8 ms.

### B. Brake-by-Wire System HLD (`SYNTHETIC_AUTOSAR_Brake_By_Wire_HLD.pdf`)
- **Page 1: Scope & Subsystem Architecture:**
  - Revision 1.4; ASIL D allocation; dual-redundant Hall-effect brake pedal sensors; lockstep microcontrollers with diverse MPUs.
- **Page 2: Software Components & Port Matrix:**
  - `PedalSensorReader_SWC`: Dual-channel ADC polling, plausibility cross-voting, normalized pedal travel `If_PedalTravel` [0-100%].
  - `BrakeDecelArbitrator_SWC`: Arbitrates driver pedal vs ACC vs AEB requests (`If_ExternalDecelRequest`), outputs front/rear axle torque command `If_BrakeTorqueCommand`.
  - `WheelBrakeActuator_SWC`: Closed-loop PID brushless caliper clamping with ABS slip ratio regulation.
- **Page 3: Functional Flow & Fail-Safe Strategy:**
  - Sequence `FF-BBW-02`: Urgent deceleration request (-8.5 m/s^2) -> pedal override check -> caliper actuation within 12 ms -> slip modulation.
  - Fail-Safe & Watchdog: 12V primary power drop below 9.0V triggers auxiliary battery switch; Fail-Silent transition time <= 10 ms (ASIL D); hardware watchdog challenge-response every 2 ms.

### C. ADAS Camera & Radar Fusion HLD (`SYNTHETIC_AUTOSAR_ADAS_Fusion_HLD.pdf`)
- **Page 1: Scope & Adaptive AUTOSAR Context:**
  - Revision 3.0; L2+ perception combining 8-MP monocam and 77 GHz radar over 1000BASE-T1 Gigabit Ethernet; Adaptive AUTOSAR POSIX execution environment.
- **Page 2: Software Components & SOME/IP Communication:**
  - `FrontCameraTracker_SWC`: Consumes SOME/IP Event `VisionObjectTracks` (50ms period, 12 KB payload); provides `PPort_CameraTracks`.
  - `RadarClusterProcessor_SWC`: CAN-FD cluster frames; provides `PPort_RadarTargets` (20ms period).
  - `ObjectFusionArbitrator_SWC`: JPDA and track-to-track covariance intersection; outputs `PPort_FusedTrackList`.
- **Page 3: Forward Collision Warning (FCW) Flow & Degradation:**
  - Sequence `FF-ADAS-03`: Lead vehicle at 65m, relative rate -18 m/s -> Time-to-Collision (TTC) = 2.1s -> acoustic/visual FCW alert when TTC < 2.4s -> AEB command when TTC < 1.4s.
  - Degradation Policy: Snow/mud obscuring camera lens triggers blind flag -> Radar-Only Degraded Mode (+20m headway margin). Max end-to-end latency = 45 ms.
