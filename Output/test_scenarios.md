# RetailHub Test Scenarios

| ID | Requirement | Type | Scenario |
| --- | --- | --- | --- |
| TS-001 | FR-AUTH-01 | API / Integration | Register with email/mobile and password, with 6-digit OTP verification valid for 5 minutes, 60s rese |
| TS-002 | FR-AUTH-02 | API / Integration | Login and issue an RS256 JWT access token (15-min expiry) and rotating refresh token (7-day expiry) |
| TS-003 | FR-AUTH-03 | API / Integration | Role-based access control (RBAC) enforced on every API route for Customer, Cashier, Store Manager, a |
| TS-004 | FR-AUTH-04 | API / Integration | Password reset via verified OTP or email reset link; password complexity enforced: 8–64 characters w |
| TS-005 | FR-AUTH-05 | API / Integration | Lock the account for exactly 15 minutes after 5 consecutive failed logins (6th attempt returns HTTP  |
| TS-006 | FR-AUTH-06 | API / Integration | Global session revocation across all active devices upon password reset or user logout |
| TS-007 | FR-CAT-01 | API / Integration | Manager/Admin can create, update, and soft-deactivate products (SKU, name, description, category, br |
| TS-008 | FR-CAT-02 | API / Integration | Search and filter products by name, description, category, brand, and price range (with boundary val |
| TS-009 | FR-CAT-03 | API / Integration | Manage hierarchical category structure with circular reference prevention and cascade deletion restr |
| TS-010 | FR-CAT-04 | API / Integration | Bulk import/update of products via CSV with row-level validation and HTTP 207 Multi-Status partial f |
| TS-011 | FR-INV-01 | API / Integration | Maintain stock quantity, reserved quantity, and available quantity per SKU per store/warehouse |
| TS-012 | FR-INV-02 | API / Integration | Reserve stock on order creation (15-min hold) and commit on payment confirmation; restore committed  |
| TS-013 | FR-INV-03 | API / Integration | Raise automated low-stock alert when available quantity falls to or below the reorder level |
| TS-014 | FR-INV-04 | API / Integration | Support manual stock adjustments (+/-) with mandatory reason code, and inter-store transfers with in |
| TS-015 | FR-INV-05 | API / Integration | High-concurrency stock reservation protection using database row-level locking (SELECT FOR UPDATE) t |
| TS-016 | FR-CRT-01 | API / Integration | Add, update quantity, and remove items; guest cart supported via session token and automatically mer |
| TS-017 | FR-CRT-02 | API / Integration | Validate real-time stock availability and synchronize catalog price changes when items are added or  |
| TS-018 | FR-CRT-03 | API / Integration | Apply and remove coupon codes; disallow coupon stacking (only 1 coupon per order); enforce min order |
| TS-019 | FR-CRT-04 | API / Integration | Calculate subtotal, discount, GST breakup (CGST+SGST for intra-state, IGST for inter-state), shippin |
| TS-020 | FR-ORD-01 | API / Integration | Place order from cart with validated delivery address, payment method, and Idempotency-Key header |
| TS-021 | FR-ORD-02 | API / Integration | Order lifecycle state machine: CREATED -> PAID -> PACKED -> SHIPPED -> DELIVERED; customer cancellat |
| TS-022 | FR-ORD-03 | API / Integration | Customers can view order history, track live shipment status, and receive milestone notifications |
| TS-023 | FR-ORD-04 | API / Integration | Returns eligible within 7 calendar days of delivery for eligible categories; non-returnable categori |
| TS-024 | FR-ORD-05 | API / Integration | Generate and download GST-compliant invoice PDF with seller GSTIN, buyer address, HSN codes, and CGS |
| TS-025 | FR-PAY-01 | API / Integration | Integrate with external payment gateway via tokenization for UPI, Cards, Net Banking, and Cash on De |
| TS-026 | FR-PAY-02 | API / Integration | Process gateway webhooks with HMAC-SHA256 signature verification idempotently to eliminate duplicate |
| TS-027 | FR-PAY-03 | API / Integration | Initiate full and partial refunds through gateway API credited strictly to original payment source w |
| TS-028 | FR-PAY-04 | API / Integration | Never store raw PAN, expiry, or CVV (PCI-DSS compliance via client-side gateway tokenization) |
| TS-029 | FR-PAY-05 | API / Integration | Compensating automatic refund workflow when payment webhook succeeds for an order already cancelled  |
| TS-030 | FR-CUS-01 | API / Integration | Customers manage profile and multiple delivery addresses with 6-digit Indian PIN code validation and |
| TS-031 | FR-CUS-02 | API / Integration | Admin creates coupons and campaigns with flat/percentage discount, max discount cap, min order value |
| TS-032 | FR-CUS-03 | API / Integration | Loyalty rewards program: earn 1 point per ₹100 spent on paid orders; 1 point = ₹1 redemption value;  |
| TS-033 | FR-POS-01 | API / Integration | Cashier creates in-store sale via HID barcode scanner (< 300 ms lookup), auto-incrementing quantity  |
| TS-034 | FR-POS-02 | API / Integration | Split tender (Cash, Card, UPI) with cash change calculation, 80mm ESC/POS thermal receipt printing,  |
| TS-035 | FR-POS-03 | API / Integration | Offline POS resilience: buffer transactions locally in IndexedDB during network disruption and auto- |
| TS-036 | FR-NTF-01 | API / Integration | Send multi-channel notifications (Email, SMS, Push) for Order Placed, Paid, Shipped, Delivered, Canc |
| TS-037 | FR-NTF-02 | API / Integration | Notification retry with exponential backoff on provider failure, respecting customer DND and marketi |
| TS-038 | FR-RPT-01 | API / Integration | Sales reports by date range (max 365 days), store, product category, and channel (WEB, APP, POS) |
| TS-039 | FR-RPT-02 | API / Integration | Inventory valuation report (cost and retail price) and low-stock exception report |
| TS-040 | FR-RPT-03 | API / Integration | Export reports as CSV and Excel ( |
| TS-041 | NFR-01 | Business rule / Non-functional | 95% of API calls respond within 500 ms at 500 concurrent users; search within 800 ms |
| TS-042 | NFR-02 | Business rule / Non-functional | Stateless services that scale horizontally; support 10x growth without redesign |
| TS-043 | NFR-03 | Business rule / Non-functional | 99 |
| TS-044 | NFR-04 | Business rule / Non-functional | HTTPS only, passwords hashed with bcrypt/argon2, JWT expiry, input validation, protection from OWASP |
| TS-045 | NFR-05 | Business rule / Non-functional | Collect minimum personal data; support consent, correction and deletion per DPDP Act |
| TS-046 | NFR-06 | Business rule / Non-functional | No lost orders or payments; retries and idempotency for external calls |
| TS-047 | NFR-07 | Business rule / Non-functional | RPO of 1 hour and RTO of 4 hours; daily full backup and continuous log backup |
| TS-048 | NFR-08 | Business rule / Non-functional | Customer can complete checkout in 5 steps or fewer; POS sale in under 30 seconds |
| TS-049 | NFR-09 | Business rule / Non-functional | Supported browsers and OS versions as listed in section 2 |
| TS-050 | NFR-10 | Business rule / Non-functional | Modular code, at least 80% unit-test coverage on business logic, CI/CD pipeline |
| TS-051 | NFR-11 | Business rule / Non-functional | Log security events and all stock and price changes with user and timestamp |
| TS-052 | NFR-12 | Business rule / Non-functional | English at launch; UI text externalized to support Hindi/Kannada later; amounts in INR |
| TS-053 | BR-01 | Business rule / Non-functional | BR-01 (Stock Reservation & Expiry): Stock is reserved for exactly 15 minutes when an order is create |
| TS-054 | BR-02 | Business rule / Non-functional | BR-02 (Promotions & Stacking): Only one coupon code can be applied per order (stacking is prohibited |
| TS-055 | BR-03 | Business rule / Non-functional | BR-03 (Returns & Non-Returnable Goods): Returns are eligible within 7 calendar days of delivery |
| TS-056 | BR-04 | Business rule / Non-functional | BR-04 (Refund Routing): Refunds are credited strictly to the original payment source (UPI VPA, origi |
| TS-057 | BR-05 | Business rule / Non-functional | BR-05 (Taxation & Pricing): Storefront prices are tax-inclusive in INR |
| TS-058 | BR-06 | Business rule / Non-functional | BR-06 (Maximum Purchase Limits): Retail customers are restricted to a maximum of 10 units per SKU pe |
| TS-059 | BR-07 | Business rule / Non-functional | BR-07 (Cash on Delivery Limits): COD is available only for serviceable pincodes up to a maximum orde |
| TS-060 | BR-08 | Business rule / Non-functional | BR-08 (Loyalty Points Economics): Customers earn 1 loyalty point per ₹100 spent on paid orders (1 po |
| TS-061 | BR-09 | Business rule / Non-functional | BR-09 (In-Store POS Stock Commitment): POS channel transactions commit stock immediately upon billin |
| TS-062 | BR-10 | Business rule / Non-functional | BR-10 (Order Cancellation Rules): Customers can self-cancel orders in CREATED and PAID states |
