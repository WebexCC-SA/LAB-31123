

# Extra: Service apps 

Till now, you have been using your own token from developer.webex.com. This token is associated with you, and it lives only 12 hours, so it is not a long term solution for building the assistant. 

**Service Apps** are machine accounts that operate on behalf of an organization, independent of specific Webex user accounts.

You will now create a **Service App** with access to **read people from your organization** and **create devices**.

Go to **Webex for Developers**, select **My Webex Apps** and click **Create a New app**:

![developer2_1](./assets/developer2_1.png){ width="850" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

Then, select **Service App**:

![developer2](./assets/developer2.png){ width="450" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

Enter the following information:

|        	|                                     	      |
|-----------------------	|-------------------------------------------------|
| **App name**       	| CiscoLive***XXXX***                  |
| **Icon**       	| Choose one of the available options                     |
| **Description**       	| Service App for Cisco Live                      |
| **Contact Email**       	| cholland@***domain*** |
| **Scopes** | |

!!! Note
    Scopes are going to be dependant on which MCP server do you want to use.

Once you have entered the information, your screen should look similar to this:
![developer3](./assets/developer3.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

!!! Warning
    From this page, copy and save the **Client ID**, **Client Secret** and **Service App ID**, as you may need them later:
    ![developer5](./assets/developer5.png){ width="700" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

    You can already save them in your .env file:

    ![createbot6](./assets/createbot6.png){ width="500" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

### Authorize your Service App in your organization

Once the Service App is created, you will need to authorize it. Navigate to:

- [Webex Control Hub](https://admin.webex.com){:target="_blank"}

Log in using the same credentials as before:
   
| Email       	| Password                                    	      |
|-----------------------	|-------------------------------------------------|
| cholland@***domain***         	| dCloud***XXXX***!                     |

Navigate to **Management > Apps > Service Apps** select the Service App you created, and click **Authorize** and **Save**:<br/>

![developer4](./assets/developer4.png){ width="950" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

To use the newly created **Service App**, you will need to get an **Access token**. 

### Access Token

Return to **Webex for Developers**, go to **My Webex Apps** and select the newly created **Service App**:

![developer6_!](./assets/developer6_1.png){ width="800" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

In the section **Org Authorizations**, select your Organization from the dropdown. 

!!! Warning "If this section does not appear, refresh the page."

A text box to enter your **Client Secret** will appear. This way, you can generate an **access_token** for this organization:

![developer6](./assets/developer6.png){ width="900" style="display: block; margin: 0 auto; border: 1px solid lightgray; border-radius: 8px;"}

!!! Warning
    Now you can save those values in your .env file. You must have already all the needed variables:

    ![env](./assets/env.png){ width="500" style="display: block; border: 1px solid lightgray; border-radius: 8px;"}

!!! Note
    The expiration time for the access token is 14 days, while the refresh token expires in 90 days.
