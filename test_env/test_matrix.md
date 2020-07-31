| Test Type              | Testing Task                          | Notes                                                                                                                              |
|------------------------|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Create                 | User Creation                         | Create at least 15-20 users from 2-3 groups                                                                                        |
|                        |                                       | -- users options (all, mapped)                                                                                                     |
|                        |                                       | Additional groups                                                                                                                  |
| Update                 | User Update                           | Ensure group changes are handled                                                                                                   |
|                        |                                       | Test user information updates                                                                                                      |
|                        |                                       | First Name                                                                                                                         |
|                        |                                       | Last Name                                                                                                                          |
|                        |                                       | Email address                                                                                                                      |
| Delete                 | Adobe-Only Action Preserve            |                                                                                                                                    |
|                        | Adobe-Only Action Remove              |                                                                                                                                    |
|                        | Adobe-Only Action Delete              |                                                                                                                                    |
|                        | Adobe-Only Action Exclude             |                                                                                                                                    |
|                        | Adobe-Only Action Remove Adobe Groups |                                                                                                                                    |
|                        | Adobe-Only Action Write File          |                                                                                                                                    |
|                        | Adobe-only user limit                 | Ensure the Adobe-only user limit works as expected as a percentage as well as an integer                                           |
|                        | Adobe user list                       | Ensure that the --adobe-users option works as expected (especially in conjunction with the Adobe-only user limit)                  |
|                        |                                       | all users                                                                                                                          |
|                        |                                       | mapped                                                                                                                             |
|                        |                                       | specific groups                                                                                                                    |
| Strategy               | Push Strategy                         | Ensure that user creation and user info updates work with the push strategy                                                        |
| Credentials (Ignore)   | Credential Storage - LDAP             | Ensure credential storage works for all platforms listed in task #9                                                                |
|                        | Credential Storage - UMAPI            | Ensure all UMAPI-related credentials work in storage for all platforms listed in task #9                                           |
|                        |                                       | API Key                                                                                                                            |
|                        |                                       | API Secret                                                                                                                         |
|                        |                                       | Private key encryption password                                                                                                    |
|                        |                                       | NOTE: It may not be possible to test that the raw (unencrypted) private key works due to limitations in Windows Credential Manager |
| Private key decryption | Private key decryption                | Ensure that encrypted private key can be successfully decrypted         
                                                           |
<br/> Additional Testing / user-sync-config.yml <br/>

| Test Type              | Testing Task                          | Notes                                                                                                                              |
|------------------------|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Adobe Users            | exclude_identity_types                | exclude both adobe and federated IDs from a delete action (use debug log to validate)                                              |
|                        | exclude_adobe_groups                  | exclude admin console groups from a delete action (use debug log to validate)                                                      |
|                        | exclude_users                         | exclude users by username and regex from a delete action (use debug log to validate)                                               |
| Directory Users        | user_identity_type                    | Set the identity type to be used,  Try federated and Adobe ID                                                                      |
|                        | default_country_code                  | Set the country code for a CSV user to be blank.  Ensure changing country code default replaces it                                 |

<br/> Advanced Testing / user-sync-config.yml <br/>

| Test Type              | Testing Task                          | Notes                                                                                                                              |
|------------------------|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Multiple UMAPI         | < TBA >                               |                                           |
| Extension config       | < TBA >                               |                                           |
| Additional groups      | < TBA >                               |                                           |
| Post sync              | < TBA >                               |                                           |

