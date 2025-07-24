# Feature managememnt

* [Creation and configuration of feature flag in Split.io](##creation-and-configuration-of-feature-flag-in-split-io)
  * [How to create flag](###how-to-create-flag)

Sometimes it is require to have option to enable/disable feature for user or for full system. This mechanism is called Feature Flag Management. 
In Checkpoint Web App features are managed by using [Split.io tool](https://app.split.io/org/104390f0-fce3-11e9-a909-0a2317b5aaf8/ws/1049f990-fce3-11e9-a909-0a2317b5aaf8) (This tool is not available for everyone, ask your dev team leads about features). Checkpoint Web App includes Split client and all operation go through it API. Client is wrapped into utility class [SplitIoUtils](com.tta.checkpoint.apis.utils.SplitIoUtils)


## Creation and configuration of feature flag in Split.io

### How to create flag
When you have been logged in into Split.io, you will be available to navigate to the Feature menu. Feature flag navigation menu allows to review the list of feature flags associated with Checkpoint Web App, additionally, make the search and view details of each flag. To create new feature flag press on the button at top of navigation menu. In new dialog enter information about you flag:
* Name of feature flag - we suggest to use the name for flag that could provide short information about feature.
* Traffic type - there are two options for this item. We have two option: account and user. Get more details this options [here](https://help.split.io/hc/en-us/articles/360019916311-Traffic-type) 
* Owners - contains the list of user who is able to manage this feature. Suggest to add at least Administrators group
* Tags - allows to filter and combine flags into associated groups
* Description - contains more details about introduced feature flag

### How to manage flag for environment
When flag has been created it is required to define environment setup. For Checkpoint 4 environments are available:
* Dev - configuration that will applied for dev portal
* QA-PreProd - configuration is applied for test and preproduction environments
* Prod - configuration is applied for production environment
On this step we define treatments that will contain available options for flag. For example bellow you could see 2 options configured for feature flag and what options was set up for default value.

### How to manage flag for testing in case of backward compatibility or long running feature
Sometimes when feature in long development or we need to not affect on other users during the testing we can configure targeted segment for feature flag.
First of all, it is necessary to create segment that will be associate with our flag. Segment allows to setup list of keys that will be used for applying feature to logged in user.
When segment will be created you need come back to your feature flag and configure Targeting rules

## Useful classes and methods