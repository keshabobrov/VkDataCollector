## Collected dataset provided here - [Google Drive](https://drive.google.com/file/d/13puA2Nl46t_YxcBvnMUt4uJugYfWx2Ep/view?usp=drive_link)

## Data Description:
- id: User identifier.
- is_closed: Indicates whether the user profile is hidden.
- bdate: User's date of birth.
- career: Information about the user's career.
- city: Information about the user's city.
- followers_count: Number of user's followers.
- education: Information about the user's education.
- last_seen_time: Time of the user's last visit.
- last_seen_platform: Platform of the user's last visit.
- occupation: Information about the user's current occupation.
- political: User's political preferences.
- langs: Languages used by the user.
- religion: User's religious beliefs.
- sex: User's gender.
- university: Information about the user's university.
- verified: Confirmation of the user's page.
- group_member: Information about the group from which the user was taken.
- group_type: Binary variable indicating the user's political views.

## General Data Information:
- The dataset contains a large number of records - 19,621,321, allowing for extensive analysis.
- Data types include bool, float64, int64, and object.
- The total memory usage for storing the data is approximately 2.5+ GB.
- The followers_count column has an average value around 428 and a standard deviation of about 2332, indicating a variety in the number of followers among users.
- The political column has diverse values, with an average around 7145 and a standard deviation of about 2,974,171, indicating a variety in political preferences among users.
- The group_type column has values 1 and 2 with different numbers of entries.

## Missing value:
Some columns, such as education, contain missing values, which may require additional data processing.

## Values description:
### Gender and City of Users:
- The sex column indicates a variety of user genders.
- Information about user cities (city) can be useful for analyzing the geographical distribution of users.

### Diversity in Political Preferences:
- The political column shows a variety of values, indicating a wide range of political views among users.
- The most common political preference values are 3 (moderate), 4 (liberal), and 2 (socialist).

### Presence of Non-standard Values:
- The political column contains non-standard values, such as 666 (likely an error) and 1,874,919,000, which may require additional data processing.

### Users with Different Political Beliefs:
- The political column includes users with diverse political beliefs, which can be interesting for further analysis of social and political trends.

### Distribution by group_type
- Most users have group_type equal to 1 (users with pro-government political views), indicating a slight predominance of users supporting government political views.

### Value of the group_type Variable
- The group_type variable is binary (1 or 2), allowing for the analysis of users' political preferences in the context of their relationship to government authority.

## Importance of the group_type Variable for Analysis:
The group_type variable can be a significant indicator for understanding the political atmosphere and social dynamics in the network, as well as for identifying differences in users' political views.

These conclusions help deepen the understanding of users' political preferences on the VK social network and reveal differences in attitudes towards government authority and opposition views among users.
