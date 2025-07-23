When testing API endpoints locally, you'll need a Bearer token for authentication. Follow these steps to obtain one from the checkpoint system:

Step-by-Step Instructions
-------------------------

### 1. Access the Checkpoint System

*   Navigate to **[https://checkpoint.ci.thomsonreuters.com](https://checkpoint.ci.thomsonreuters.com/)**
*   Log in using your standard credentials

### 2. Open Developer Tools

*   Once logged in, **right-click** anywhere on the page
*   Select **"Inspect"** from the context menu
    *   _Note: This option is typically at the bottom of the menu in most browsers_

![Screenshot 2025-06-18 150257.png](/.attachments/Screenshot%202025-06-18%20150257-84f7997d-1d1b-4b4d-9a84-6a73a80d82ce.png)

### 3. Navigate to Application Storage

*   In the Developer Tools panel that opens, locate and click the **"Application"** tab
    *   _This is usually found in the top toolbar, often as the rightmost option_
*   If the panel is too small, **expand it** by dragging the edges for better visibility

![Screenshot 2025-06-18 150433.png](/.attachments/Screenshot%202025-06-18%20150433-7d40cdbf-be8d-4bd5-8525-665645f5f23a.png)

### 4. Access Cookies

*   In the left sidebar, in the **"Storage"** section, click on **"Cookies"**
*   Select **"[https://checkpoint.ci.thomsonreuters.com](https://checkpoint.ci.thomsonreuters.com/)"** from the dropdown

![Screenshot 2025-06-18 150830.png](/.attachments/Screenshot%202025-06-18%20150830-3aa6a6c1-f8ae-4033-b834-a7570539aacc.png)

### 5. Find the Access Token

*   Use the **search bar** at the top of the cookies table
*   Type: `cp_access_token`
*   The token will appear in the search results

![Screenshot 2025-06-18 150951.png](/.attachments/Screenshot%202025-06-18%20150951-a48db4c0-4a01-4aab-9564-385f83b4ce91.png)

### 6. Copy the Token

*   **Copy the value** from the "Value" column next to `cp_access_token`
*   This is your Bearer token

Using the Token
---------------

You can now use this token for API authentication in:
*   **Postman**: Add as Authorization header with type "Bearer Token"
*   **Direct API calls**: Include in the Authorization header as `Bearer [your-token]`
*   **Local development**: Use in your application's API requests

Important Notes
---------------

*   ⚠️ **Security**: Keep your token secure and never share it publicly
*   ⏰ **Expiration**: Tokens may expire, so you might need to repeat this process periodically
*   🔄 **Refresh**: If API calls return authentication errors, generate a new token