from haystack import Document

from pipelines import create_storing_regulation_pipe

regulations = """
Rules and Regulations for Inventory Management System
1. Purpose and Scope
The Inventory Management System (IMS) is designed to ensure the accurate tracking, monitoring, and control of inventory within an organization. All employees interacting with the IMS must adhere to these rules and regulations to maintain system integrity and ensure operational efficiency. These rules apply to all personnel responsible for inventory procurement, handling, and documentation.
2. User Access and Authentication
Access to the IMS is restricted to authorized personnel only. Each user must have a unique login ID and password, which should not be shared. Users are required to follow organizational cybersecurity guidelines, including regular password updates and reporting unauthorized access attempts.
3. Data Entry and Accuracy
All inventory-related data must be entered into the IMS promptly and accurately. This includes details such as product descriptions, quantities, serial numbers, and dates of acquisition. Errors or omissions must be corrected immediately upon detection, and repeated inaccuracies may result in disciplinary actions.
4. Inventory Categorization
All items in the inventory must be classified according to predefined categories, such as raw materials, finished goods, or office supplies. Each item must be labeled with a unique identifier to facilitate tracking and reporting. Misclassification of items is strictly prohibited and may disrupt operational workflows.
5. Stock Levels and Reordering
The IMS must be used to monitor stock levels and generate alerts for reordering when thresholds are reached. Employees must ensure stock replenishment requests are submitted and approved in a timely manner to prevent shortages or overstocking.
6. Audits and Inspections
Periodic audits and inspections of inventory must be conducted to verify system data against physical stock. Discrepancies must be documented and reported to management immediately, along with a proposed resolution plan. Users involved in audits are expected to cooperate fully.
7. Handling and Storage
Inventory items must be handled with care and stored according to specified guidelines. Users must update the IMS to reflect any changes in location or condition of items. Damaged or obsolete items must be reported immediately, and their removal must be authorized by management.
8. Compliance with Legal and Regulatory Standards
All activities related to inventory management must comply with relevant legal and regulatory standards. Users must be familiar with applicable laws and ensure that procurement, storage, and disposal processes align with these requirements.
9. Training and Support
All users must undergo mandatory training on the use of the IMS, including updates or new feature releases. Support for technical issues or operational queries will be provided by the designated IT department or system administrator.
10. Accountability and Penalties
Users are accountable for the accuracy and timeliness of the data they input into the IMS. Any misuse or deliberate manipulation of the system is strictly prohibited and will result in disciplinary action, which may include termination of employment or legal consequences.
By adhering to these rules and regulations, the organization ensures the efficient and reliable operation of the Inventory Management System, supporting overall business objectives and customer satisfaction.
"""

storing_pipe = create_storing_regulation_pipe()

response = storing_pipe.run(
    {"splitter": {"documents": [Document(content=regulations)]}}
)

print(response)
