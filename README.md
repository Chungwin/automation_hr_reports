# HR Report Automation (HiBob and Google Sheets)
The following scripts automate the workflows for generating, archieving, formatting HR reports generated in the HR System **[HiBob](https://www.hibob.com/)**. For the sake of better data visibility and accessibility for HR professionals, Google Drive and Google Sheets are used as database/storage. Google Sheets is an easy and uncomplicated data soource for Tableau, which is used for data visualization and reporting. One of the main advantages using Google Sheets together with Tableau is, that allows to easily edit and write data. Editing data on the fly when using a dwh requires a more programatic approach. Google Sheets lowers this barrier significantly.

The following scripts connect to the **[HiBob](https://www.hibob.com/)** API deal with Time-off exports (csv). 

## What does the programme do?
- For the holiday-report, the programme looks into a local directory for the latest csv export, uploads it to Google Drive to archieve it, and updates a given Google Sheet to display the latest holiday balance.
- For the general report, I created an individual report in HiBob, connect to the respective API, and archieve / upload the informations. (Not pushed yet).
- All further reporting steps are done with Tableau.

Much more to come!

## Installation & Setup
- Install Python
- In order to access the Google APIs for Drive and Sheets, access with your Google account the **[Google Develoepr Console](https://console.cloud.google.com/)**, create a project, enable the Drive and Sheets APIs, and create and download Service Account credeintails (for Sheets API) and OAuth client ID credentials (for Drive API). A nice walkthrough video for setting up your google accout to connect to Google sheets can be found **[here](https://www.youtube.com/watch?v=4ssigWmExak&t=1028s)**. 
- For this project, I already created a folder to archieve my reports and a spreadsheet within Google Drive. You can see me referencing their IDs as environment variables. 
- Make sure you invite your Google Service Account (with editor rights) to all folders and files you create in Google Drive.

## Documentations
- **[HiBob API](https://help.hibob.com/hc/en-us/articles/4557125039505-Getting-started-with-APIs)**
- **[Google Sheets API](https://developers.google.com/sheets/api/reference/rest)**
- **[Google Drive API](https://developers.google.com/drive/api/v3/reference)**


## License

MIT
**Free Software, Hell Yeah!**