# Cloud-Provider-Advisor

Nowadays, many organizations are shifting their infrastructure towards cloud mainly because of enhanced cost-savings as they don’t need to spend money on maintaining on premise infrastructure, and also because of the ability to scale up or scale down instantly. And then there are other features such as improved data security, better data recovery, and improved reliability and availability.
With so many options available in the market, it can become difficult to choose the right cloud service provider as it requires considering many factors such as security standards and practices followed by the provider, technologies that meet the workload requirements, data laws of the location where the datacentre of the provider is located, service level agreements, etc. Cost is another such factor which is important to consider before choosing a cloud service provider. The customer should not pay for more than what they require. For this problem, we propose an application which accepts the compute requirements such as the number of vCPUs, memory, storage, operating system, region, etc. from the user and suggests the most economical cloud service provider to the user after comparing the offers provided by different cloud providers. For this application we are considering the compute services provided by AWS, Microsoft Azure and Google Cloud Platform.

### The purpose of this project is to provide a single portal to view the compute resources offered by the major cloud providers and simplify the process of selecting them by gathering the requirements of the user and showing them the appropriate options.

### The target beneficiaries of the proposed methodology are small and medium enterprises as they have specific requirements and are constrained in how much they spend to fulfil these requirements and need to avoid paying for extra resources which they do not require.

### The scope of this project is to make it easier to compare virtual machines offered by different cloud provider like AWS, Microsoft Azure and GCP. The user will specify their requirements of virtual machine based in which a list of appropriate machines will be generated.

## Features
The system will have an organized process to retrieve the virtual machine instance data from the respective APIs and store it in a database. The data will then be presented to the user via a user-friendly interface. This system will provide searching facilities based on various features such as memory, storage, price, etc.

### Structure of the application
<img width="1317" alt="Screenshot 2023-06-08 at 4 34 48 PM" src="https://github.com/Kunal2703/Cloud-Provider-Advisor/assets/78562069/0d35e147-c619-43f8-aabd-c7a7d108fc96">

### GUI of the application
<img width="1328" alt="Screenshot 2023-06-08 at 4 37 40 PM" src="https://github.com/Kunal2703/Cloud-Provider-Advisor/assets/78562069/d0fa8079-cd9d-4bbc-b8f9-b00b106f688d">

## Important link:
### SDK- Software Development Kit is set of tools provided by the developer to a third party which can be used in producing applications using a particular platform.
<br>
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
<br>
https://azure.github.io/azure-sdk-for-python/
<br>
https://cloud.google.com/python/docs/reference

### API- Application Programming Interface is a component or a mechanism that allows applications or software to communicate with each other.
<br>
https://learn.microsoft.com/en-us/rest/api/cost-management/retail-%20prices/azure-retail-prices
