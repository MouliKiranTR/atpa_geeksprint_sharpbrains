
## Goal & Objectives
### Background

In topic pages for Federal and State practice areas, each topic pages has a  type-ahead filter that enhances user experience by allowing users to quickly identify available topic pages based on their input keywords.
The current search functionality does not provide the level of flexibility required, as it only matches the beginning of words. The new filtering mechanism should respect any match within the topic and subtopic names.

### Objective
The objective of this spike is to explore the feasibility of implementing a keyword search filter on the topic selection page that filters topics and subtopics based on user input, regardless of the position of the keyword within the title.

### User Acceptance Criteria
##Filter Availability

When a user is on a Federal or State Topic Page, they will see a search filter in the Topic Page section.
##Keyword Input

When the user types any keyword into the search filter, the system will instantly filter the topic and subtopic names to display only those that contain the entered keyword, irrespective of its position in the title.

##Existing Functionality with bento control for Table of contents
![image.png](/.attachments/image-42fda5be-16b4-41e4-bea2-eaa9177ae359.png)
## Controls With Safforn
https://saffron.thomsonreuters.com/?path=/docs/components-search-field--docs
![image.png](/.attachments/image-b2fc2b18-8e75-4ae5-b26d-fcc311f28b9a.png)
##How to implement
our tree data is like
![image.png](/.attachments/image-4a4dde80-a29c-4a17-9777-b6a0d023fe3c.png)
take variable topicdetail and use  topicsResponse property to copy that data and apply filter on that array which gives filter data 

####add span for display text
<span [innerHTML]="highlightText(topic.name)"></span>

 <a target="_parent" (click)="onSubtopicClick(subtopic)" [innerHTML]="highlightText(subtopic.name)"></a>
####add highlightText function 

there is also hit class available for display highlight text which can use 

highlightText(text: string): string {

    if (!this.searchTerm) {
      return text;
    }

    const regex = new RegExp(`(${this.searchTerm.split('').join('|')})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
  }
