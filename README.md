# CertifyX - SaaS Platform for Internship Certificate Generation & Verification

## Problem Statement

### The Current Problem
Currently, when students complete an internship, companies usually provide them a certificate as proof of completion. But in many cases, this certificate is created manually using Word or design tools. Here’s how it usually works:

1. The company types out each student’s name and other details manually in a Word file.
2. They generate a PDF for each certificate.
3. A unique ID is assigned manually to each certificate.
4. The company emails or shares the certificate individually with each student.
5. There is no proper tracking of how many certificates have been created or shared.
6. If someone wants to verify whether a certificate is genuine, they must call or email the company — there is no easy way to do it online.

This manual process is slow, tiring, and completely dependent on a single person in the company. If that person is on leave or unavailable, the certificate work gets blocked. Additionally, as the number of students increases, it becomes very difficult to handle this manually. Moreover, if multiple people across different departments want to generate certificates at the same time, it is not possible. This makes the system non-scalable, creating delays and confusion.

### Major Pain Points
- Time-consuming manual process
- Human-dependent, leading to delays
- Difficult to track or manage certificate records
- No way to verify certificates online
- Non-scalable as the number of certificates increases
- No reports or dashboards to see how many certificates have been issued, pending, etc.

## What We Want to Build

To solve this problem, we want to build a SaaS-based (Software as a Service) platform that automates the entire process of certificate generation.

### Features & Functional Modules
1. **Authentication & User Management**  
   - Register an account with basic info like company name, email, phone number, and password.
   - Login/logout securely.
   - Reset password with optional admin approval for new companies.

2. **Subscription & Pricing Plans**  
   - Multiple pricing tiers based on the number of certificates needed monthly.
   - Payment integration (mock payment gateway).

3. **Template Management**  
   - Companies can upload custom certificate templates.
   - Define dynamic fields (e.g., Name, Course, Date).

4. **Candidate Management (CRUD)**  
   - Add candidates manually or upload bulk data via Excel.
   - View, edit, and delete candidate records.

5. **Certificate Generation**  
   - Auto-generate certificates with unique IDs and QR codes.
   - Certificates are downloadable or sent via email.

6. **Certificate Verification**  
   - Public page for certificate verification by entering ID or scanning QR code.

7. **Dashboard & Reporting**  
   - Dashboard for tracking certificate usage, remaining quotas, and templates used.
   - Reports with charts and usage statistics.

8. **Profile & Account Settings**  
   - Companies can update their profile, view subscription details, and change passwords.

9. **Admin Panel (Super Admin)**  
   - Manage all company accounts and subscription plans.
   - Track company certificate usage and manage reports.

## Target Users
- **Super Admin (Platform Owner)**: Manages platform settings, billing, user issues.
- **Company Admin (Client)**: Manages templates, certificate generation, team access.
- **Recipient / Verifier**: Receives certificates or visits the platform to verify authenticity.

## Tech Stack
- **Backend**: Python + Django
- **Frontend**: HTML, CSS, JavaScript (Bootstrap)
- **Database**: MySQL
- **Versioning**: Git + GitHub
- **File Storage**: Local/Cloud (initially local file system for certs)
- **Payments**: Razorpay/Stripe/Paypal (mocked for now)
- **QR Generator**: Python library like `qrcode`
- **PDF Generator**: Reportlab/WeasyPrint/wkhtmltopdf

## Bonus Features (Optional)
- Auto-email with PDF attachment
- Role-based access to certificate generation for company teams
- Expiry alerts to company email
