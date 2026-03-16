# Creating a New User in SAP

This document describes the steps required to create a new user in an SAP system using the **SU01 transaction**.

---

## Prerequisites

- You must log in to the SAP system using an **existing user account with administrative privileges**.
- The user performing this operation must have authorization to execute the **SU01 transaction**.

---

## Steps to Create a New User

### 1. Login to SAP
Log in to the SAP system using an existing account that has the required privileges to create and manage users.

---

### 2. Open the User Maintenance Transaction
In the **Transaction Command Box**, enter:  ```SU01```

- If an error occurs while executing this transaction, it likely indicates that your user account does **not have sufficient authorization**.

---

### 3. Enter the Username
Once the **User Maintenance screen** appears:

1. Enter the **new username** in the *User* field.
2. Click **Create** to begin the user creation process.

---

## 4. Maintain User Details

After clicking **Create**, several tabs will be available to configure the user's information.

---

### 4.1 Address Tab

Provide the basic user information:

- **First Name**
- **Last Name**
- **Email Address**

This information helps identify the user within the system and is often used for notifications.

---

### 4.2 Logon Data Tab

Configure authentication-related settings:

- **User Type**
  - **Dialog** – Used for normal interactive users.
  - **Communication** – Used for external RFC connections.
  - **System** – Used for system-to-system communication or background processing.
  - **Service** – Used for shared or anonymous access scenarios.

- **Initial Password**
  - Set a temporary password for the user.
  - Typically, the user will be prompted to **change the password on the first login**.

---

### 4.3 Roles Tab

If the user requires specific access permissions, roles can be assigned in this tab.

Steps:
1. Enter the **role name(s)** required for the user.
2. Save the role assignment.

Roles determine the **authorizations and access levels** available to the user within the SAP system.

---

### 4.4 Profiles Tab

If necessary, profiles can be assigned directly to the user.

Example: ```SAP_ALL```


- This profile grants **full authorization across the SAP system**.

> ⚠️ **Note:** Direct profile assignment is generally not recommended in production environments. Roles should typically be used instead to manage permissions.

---

## 5. Save the User

After entering all required details:

1. Click **Save**.
2. The user account will be created successfully.

---

## Additional Notes

- Always follow the **principle of least privilege** when assigning roles or profiles.
- Avoid assigning powerful profiles like **SAP_ALL** unless absolutely necessary.
- Ensure the user is assigned only the **minimum required access** needed to perform their tasks.