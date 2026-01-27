# 📡 WireTapper

**Wireless OSINT & Signal Intelligence Platform**

WireTapper is a wireless OSINT tool designed to discover, map, and analyze radio-based devices using passive signal intelligence. It provides investigators, researchers, and security analysts with real-time visibility into the invisible wireless landscape around them.

WireTapper detects and correlates signals from common wireless technologies, helping users understand what devices exist, where they are likely located, and how they interact, without active intrusion.

## 🚀 Installation

Follow these steps to get WireTapper up and running:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/WireTapper.git
   cd WireTapper
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r WireTapper.txt
   ```

3. **Configure API Keys:**
   For security, it is recommended to use environment variables. You can set them in your terminal or use a `.env` file:
   ```bash
   export WIGLE_API_NAME="your_wigle_api_name"
   export WIGLE_API_TOKEN="your_wigle_api_token"
   export OPENCELLID_API_KEY="your_opencellid_api_key"
   export SHODAN_API_KEY="your_shodan_api_key"
   ```
   Alternatively, you can edit the hardcoded values in `app.py` (not recommended for production).

4. **Run the application:**
   ```bash
   python app.py
   ```
   After running the app, open in your browser: `https://127.0.0.1:8000/map-w`

## 📶 Supported Signal Intelligence

WireTapper can identify and analyze signals from:

*   **Wi-Fi** access points & clients
*   **Bluetooth & BLE** devices
*   **Wireless CCTV / IP cameras**
*   **Vehicles** broadcasting RF signals (infotainment, telemetry, keyless systems)
*   **Headphones, wearables**, and smart devices
*   **Smart TVs & IoT** appliances
*   **Cell towers** & mobile network beacons
