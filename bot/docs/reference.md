# Bot Reference

## Commands

### add reports admin `member:Member`

For guild admins

It gives the reports admins role to the member.

### remove reports admin `member:Member`

### send report `member:Member`

For everyone

It sends a modal where user should enter report text message and after it creates ticket channel in configurable category. Bot must adds in ticket channel interaction author and send buttons to interact with report.

### close report

For reports admins

It gets close reason from the author and closes the report, deletes the channel, and send logs to logs channel.

### set report tickets category `category:Category`

For reports admins

It sets the category where bot will creates ticket channels.

### enable reports

For reports admins

### disable reports

For reports admins

### add member to report ticket `member:Member`

It adds member to the channel.

### remove member from report ticket `member:Member`

It removes member to the channel.

### set reports logs channel `channel:Channel`

### enable logs

### disable logs

### enable log type `type:String`

It enables log type ect. reports logs channel will receives logs with the type

### disable log type `type:String`

### log types

For reports admins

It sends logs' types.

## About log types

There are types of logs:

- `REPORT_SENDED`
- `REPORT_CLOSED`
- `MEMBER_ADDED_TO_REPORT_TICKET`
- `MEMBER_REMOVED_FROM_REPORT_TICKET`
- `REPORTS_ADMIN_ADDED`
- `REPORTS_ADMIN_REMOVED`
