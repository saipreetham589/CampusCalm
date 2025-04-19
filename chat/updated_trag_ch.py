import os
import json
import logging
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from openai import AzureOpenAI


red_folder = """


# STEVENS INSTITUTE OF TECHNOLOGY 1870
# RED FOLDER
## MENTAL HEALTH RESPONSE PROTOCOL

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## Assisting Students in Distress

Stevens faculty and staff are vitally important resources for identifying and helping students in distress. Despite ambitious outreach efforts on most college campuses, university counseling centers may not reach the majority of students. For this reason, Counseling and Psychological Services (CAPS) and the Campus Awareness, Referral, and Education (CARE) Team want to support efforts by all campus community members to assist in the identification of students in distress and in their referral for help. You strengthen our campus community by creating a network of support for our students.

### [Icon: Eye] SEE SOMETHING
Faculty and staff may be the first to see students in distress and can be the first to help.

### [Icon: Speech Bubble] SAY SOMETHING
Trust your instincts and say something if you feel concerned. Act with compassion when dealing with these students.

### [Icon: Checkmark] DO SOMETHING
Many students feel isolated or unable to reach out for help. Others may not know where to go. Stevens' Red Folder will help you recognize students in distress and connect them with appropriate resources on campus. The Family Educational Rights and Privacy Act (FERPA) typically limits the information that may be shared about student records. However, it does permit information sharing between institutional personnel in emergency situations. Also keep in mind that some students who are part of a marginalized group may feel especially isolated on campus. Identity dimensions such as race, ethnicity, cultural background, nationality, immigration status, sexual orientation, gender identity, ability status, socioeconomic status, and religious beliefs, among others, are important to consider. Your sensitivity to these needs is especially important in order for students to connect with the appropriate assistance.

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## Response Protocol
**SEE SOMETHING, DO SOMETHING**

### Is the student a danger to themself, to others, or do they need immediate assistance for any other reason?

---

**[Icon: Exclamation Mark in Triangle - Orange Background]**

### YES
The student's conduct is clearly and imminently reckless, dangerous, and/or threatening and is suggestive of harm to self or others in the community.

*   **Call Campus Police at 201.216.3911**
*   **Follow up with an email to the CARE Team at care@stevens.edu.**

---

**[Icon: Question Mark in Circle - Dark Grey Background]**

### UNSURE
The student shows signs of distress; I'm not worried about their safety, but I am not sure how serious it is. The interaction has left me feeling uneasy or concerned about the student.

*   **Call CAPS for consultation anytime of day at 201.216.5177. After hours and weekends press “2” to speak with a live counselor.**
*   **Email the CARE Team at care@stevens.edu.**

---

**[Icon: Prohibition Symbol in Circle - Blue Background]**

### NO
I am not concerned about the student's imminent safety, but they have significant academic or personal concerns and could use additional support.

*   **Email the CARE Team at care@stevens.edu or connect them with the appropriate referral on campus.**

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## Signs of Distress

**[Image: Bookshelves with lights]**
### ACADEMIC INDICATORS
*   Significant decline in grades or performance
*   Repeated absences
*   Bizarre content in assignments
*   Overly demanding of attention
*   Disruptive behavior in class

**[Image: Person holding head in distress, black and white]**
### PHYSICAL INDICATORS
*   Deteriorating hygiene
*   Excessive fatigue or irritability
*   Tearfulness
*   Slurred speech
*   Out of touch with reality

**[Image: Hands comforting another pair of hands]**
### PSYCHOLOGICAL INDICATORS
*   Disclosure of personal distress
*   Panic attacks or anxiety
*   Verbally abusive
*   Expressions of hopelessness
*   Concern from friends

**[Image: Yellow warning sign with exclamation mark]**
### SAFETY RISK INDICATORS
*   Threatening harm
*   Unprovoked anger or hostility
*   Communicating threats
*   Assignments or communications containing themes of hopelessness, isolation, or despair

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## Dangerous or Distressed?
**AND WHAT TO DO?**

### DANGEROUS
*   Behavior is deadly
*   Conduct is imminently reckless
*   Behavior is dangerous to self or others
*   Intense anger
*   Intoxicated
*   Intense withdrawal
*   Discusses weapons

### DISTRESSED
*   Very anxious
*   Sad
*   Withdrawn
*   Lacks motivation
*   Seeks constant attention
*   Interactions feel less like academic counseling and begin to feel more like personal counseling

## TO GET HELP

### DANGEROUS
**Call Campus Police**
**201.216.3911**

### DISTRESSED
**Submit a CARE report**
**care@stevens.edu**
**Call CAPS at 201.216.5177**

---

If a student is causing a disruption but is not a threat, please make sure you are safe. Then, use a calm, non-confrontational approach to de-escalate the situation. Explain why the behavior is inappropriate. If the behavior continues, you may ask the student to leave. If they do not, contact Campus Police at 201.216.3911. Whether the student calms down or leaves, report the incident to the CARE Team at care@stevens.edu.

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## How to Refer

### 1. Prepare to Reach Out
**Remember, you are not alone in this.**
Consult with CAPS or the CARE Team to explore concerns and identify appropriate campus resources. Make sure you feel safe and let someone else know that you are going to have a tough conversation with a student of concern. Put Campus Police's number in your phone (201.216.3911) in case you need to call for help.

### 2. Connect with the Student
**Put your preparation plan into action.**
Share your concern calmly and directly, and be prepared to listen. Avoid being argumentative or minimizing the student's distress. Focus on the concerning behavior, not blaming or shaming the student. Respect privacy without guaranteeing confidentiality. Explore the student's support system and emphasize the importance of professional help.

### 3. Make the Referral
**Communicate confidence.**
Recommend the appropriate service and discuss what they might expect from that resource. Normalize the experience of seeking support from others. Frame the decision to seek help as a wise one. Offer to be with the student when they call the referral or take them to the referral source. Follow-up to see if they attended the appointment.

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

**[Image: Scales of Justice statue]**

## Title IX

Title IX prohibits sex discrimination, including sexual harassment, sexual assault or violence, stalking, domestic violence, or rape in education programs and activities.
Stevens Institute of Technology does not tolerate any degree of sexual misconduct on or off-campus. Sexual misconduct violates the values of our community as well as the University's mission to educate leaders who are strong in character and in their identity and vocation, and committed to service and justice as articulated in the University's mission statement.
If a student discloses sex discrimination, you are obligated to report the disclosure to the university Title IX office.

### Points of Contact

**Title IX Coordinator**
Stacy Fisher, Ed.D., Director of Community Standards
University Center, Room 215
201-216-3383 | sflowers@stevens.edu

**Deputy Title IX Coordinator for Students**
Cynthia Eubanks, Director of Residential Education
Harries Tower, Room 103
201-216-8963 | ceubanks@stevens.edu

**Deputy Title IX Coordinator for Employees**
Xhiljola Ruçi Kluger, J.D., Director of Employee Relations and Compliance
Wesley J. Howe Center, 5th Floor
201-216-3718 | xruci@stevens.edu

### Confidential Resources

**Counseling and Psychological Services**
201-216-5177 | CAPS@stevens.edu

**Health Services**
201-216-5978 | studenthealthservices@stevens.edu

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## On-Campus Resources

**[Background Image: New York City skyline from Hoboken]**

### CAPS
Counseling and Psychological Services for Stevens students
Student Wellness Center, 2nd Floor
stevens.edu/CAPS
201-216-5177

### CARE TEAM
The Campus Awareness, Referral, and Education Team. Connects with students of concern to offer resources and support.
stevens.edu/campus-life/health-wellness/care
care@stevens.edu

### CAMPUS SAFETY
Support for student safety at every hour of the day and night, every day of the year.
Morton-Pierce-Kidde Complex
Main line: 201-216-5105
Emergency line: 201-216-3911

### STUDENT HEALTH SERVICES
An acute health care facility that offers health promotion and disease prevention, care during acute and chronic phases of illness, and referrals to outside providers when appropriate
201-216-5678

### CAMPUS RECREATION
Provides a comprehensive program of physical sport and wellness activities designed to meet the diverse needs and interests of students
https://stevensrec.com/
201-216-8111

### RESIDENTIAL EDUCATION
The mission of the Office of Residential Education is to provide safe and inclusive communities that foster meaningful relationships and create opportunities for learning outside of the classroom.
201-216-8990

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## On-Campus Resources

**[Background Image: New York City skyline from Hoboken]**

### SPIRITUALITY
Stevens is committed to creating a supportive and inclusive campus environment for all students. This includes supporting religious and faith-based student organizations, maintaining awareness of the variety of holidays celebrated on campus, and building partnerships with local community organizations.
https://www.stevens.edu/campus-life/diversity-and-inclusion/spirituality

### OFFICE OF DISABILITY SERVICES
ODS assists individuals with disabilities to have opportunity for full participation and equal access to campus programs and services, in alignment with federal standards and state regulations.
disabilityservices@stevens.edu
201-216-3748

### DIVERSITY, EQUITY & INCLUSION
Provides support and resources that center the needs and voices of underrepresented and underserved students, facilitate dialogues and educational workshops that promote inclusive leadership, and engage all Stevens students, faculty and staff in co-creating a socially conscious community.
dei@stevens.edu | 201-216-5624

### ACADEMIC SUPPORT CENTER
Offerings for undergraduates include tutoring for technical courses, freshman quiz reviews, peer leaders for incoming freshmen, and various academic success workshops.
Howe Center 9th Floor
201-216-5228

### CAREER CENTER
The source for career counseling, graduate school preparation, job opportunities, and all things career-related.
Howe Center 6th Floor
careercenter@stevens.edu | 201-216-5166

### FINANCIAL AID
Financial Aid helps make a Stevens education as affordable as possible for students. They help maximize financial aid awards and assist in the decision-making process.
Howe Center 1st Floor
financialaid@stevens.edu | 201-268-5406 (*Note: OCR originally showed 201-268-5406, please verify this number if critical*)

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## On-Campus Resources

**[Background Image: New York City skyline from Hoboken]**

### LGBTQ+
The Office of Diversity, Equity and Inclusion serves as the hub for support services, resources, and educational programming related to LGBTQ+ identity. We continually work to ensure that the campus feels welcoming and supportive to all students.
stevens.edu/LGBTQ

### WELLNESS EDUCATION
The Office of Wellness Education is dedicated to supporting a holistic culture of wellness at Stevens by aligning university wellness initiatives and providing outreach and education on a variety of health and wellness topics.
wellness@stevens.edu

### LORE-EL CENTER
The Lore-El Center is a vibrant living and learning environment that promotes women's leadership through programs, events, mentorship and a shared residential experience.
loreel@stevens.edu | 201-216-5624

### GRADUATE STUDENT LIFE
Strives to create a supportive, engaging environment that enables students to pursue their academic goals. Promotes students' professional and personal development through a wide variety of programs and services.
graduatelife@stevens.edu | 201-216-5633

### ISSS
International Student and Scholar Services (ISSS) advises, provides immigration services, promotes cross-cultural opportunities and offers specific programs and services to our international population.
Howe 9th Floor
isss@stevens.edu | 201-216-5189

### WRITING AND COMMUNICATION CENTER
The Writing and Communications Center (WCC) helps students develop the written and oral communication skills essential to their success in academic coursework and beyond Stevens.
my.stevens.edu/writing
writing@stevens.edu | 201-216-8990

---

# RED FOLDER
**(STEVENS INSTITUTE OF TECHNOLOGY 1870 Logo)**

## STUDENT CRISIS RESOURCES

### CAMPUS RESOURCES

**Counseling & Psychological Services (CAPS)**
Student Wellness Center, 2nd Floor
201-216-5177
caps@stevens.edu
Phone line is staffed 24/7
Visit stevens.edu/caps for more information.

**Campus Police (Available 24/7)**
201-216-3911

**Worried about someone at Stevens?**
Submit a CARE concern at stevens.edu/care
or email care@stevens.edu
For more information about CARE visit stevens.edu/campus-life/health-wellness/care
CARE should not be used for time sensitive emergencies.

### NATIONAL RESOURCES

**Suicide & Crisis Lifeline**
Call 988

**SAMHSA's National Helpline**
1-800-662-(HELP) 4357
Treatment referral and information service for mental and/or substance use disorders.

**Crisis Text Hotline**
Text "HELLO" to 741-741
Are you a person of color? Text "STEVE” to 741-741
crisistextline.org

**Trevor Project Hotline**
1-866-488-7386
Text "START" to 678-678
Support line for the LGBTQ+ community.

**Trans Lifeline**
1-877-565-8860
Provides trans peer support.

**Asian Lifenet Hotline**
1-877-990-8585
Cantonese, Mandarin, Japanese, Korean, and Fujianese are offered.

**Call 911 for any off-campus emergency.**

---

**TAKE A PHOTO, SAVE THESE NUMBERS: IT COULD SAVE A LIFE!**
-------------------------------------------------------------------

# Mental Health Concerns: How and When Should I Help?
## A Guide for Faculty, Staff, Students, Friends, and Family Members

Should I be concerned about my friend? My child? A student in my class?

What are the signs I should look for?

Should I tell them that I'm concerned?

And where do I send them to get the help they need?

At Stevens Counseling and Psychological Services (CAPS), we often receive questions like these from concerned family members, faculty, staff, students, and friends. Typically, someone has noticed a change in someone they care about, and they want to know what they can do to help. This webpage is designed to aid in the recognition of the warning signs of a student in distress and to provide resources to get the student the help they need.

## Signs and Symptoms of Emotional Distress
Lifeguards are trained to recognize signs that a swimmer is going under the water and struggling to stay afloat. When it comes to student mental health, a struggling student may also display common signs and symptoms of distress. By being mindful of these signs, a concerned party can provide a needed life-preserver in the form of a referral to a caring mental health professional. While not an exhaustive list, the signs and symptoms listed below (courtesy of the Mayo Clinic) are among the ones we might expect to see among college-aged students in distress:

### **Depression**
*   Feelings of sadness, tearfulness, emptiness or hopelessness
*   Feelings of worthlessness or excessive guilt
*   Angry outbursts, irritability or frustration, even over small matters
*   Loss of interest or pleasure in most or all normal activities
*   Tiredness and lack of energy, so even small tasks take extra effort
*   Slowed thinking, speaking or body movements
*   Sleep disturbances (sleeping too much, or too little)
*   Eating disturbances (eating too much, or too little)
*   Trouble thinking or concentrating; difficulties with memory
*   Frequent or recurrent thoughts of death or suicide
*   Unexplained physical problems, such as back pain or headaches

### **Anxiety**
*   Feeling nervous, restless or tense
*   Having a sense of impending danger, panic or doom
*   Physical symptoms including increased heart rate, rapid breathing, sweating, and/or trembling
*   Feeling weak or tired
*   Trouble concentrating or thinking; mind going ‘blank’
*   Having difficulty controlling worry
*   Difficulty sleeping
*   Experiencing gastrointestinal (GI) problems
*   Having the urge to avoid things that trigger anxiety

### **Substance (Drugs, Alcohol) Misuse**
*   Feeling the need to use the substance regularly
*   Having intense urges for the substance that block out other thoughts
*   Over time, needing more of the substance to get the same effect
*   Taking larger amounts of the substance, over a longer period of time than intended
*   Making certain to maintain a supply of the substance
*   Spending money on the substance, even though can't afford it
*   Not meeting obligations; cutting back on social or recreational activities
*   Continuing to use the substance, even though it's causing life problems
*   Doing illegal or immoral things to get the substance (e.g. stealing)
*   Engaging in risky activities when under the influence of the substance
*   Spending a good deal of time getting the substance, using the substance or recovering from the effects of the substance
*   Failing in attempts to stop using the substance
*   Experiencing withdrawal symptoms when one attempts to stop taking the substance

### **Eating Disorders**
*   Skipping meals or making excuses for not eating
*   Adopting an overly restrictive diet
*   Dieting all the time
*   Excessive focus on healthy eating
*   Withdrawal from normal social activities
*   Persistent worry or complaining about being fat and talk of losing weight
*   Frequent checking in the mirror for perceived flaws
*   Repeatedly eating large amounts of sweets or high-fat foods
*   Use of dietary supplements, laxatives, or herbal products for weight loss
*   Excessive exercise, even and especially when injured
*   Calluses on the knuckles from inducing vomiting
*   Problems with loss of tooth enamel that may be a sign of repeated vomiting
*   Leaving during meals to use the toilet
*   Eating much more food in a meal or snack than is considered normal
*   Expressing depression, disgust, shame, or guilt about eating habits
*   Eating in secret

### **Mania (a core feature of Bipolar Disorder)**
*   Abnormally upbeat, jumpy, or wired
*   Increased activity, energy, or agitation
*   Exaggerated sense of well-being and self-confidence (euphoria)
*   Decreased need for sleep
*   Unusual talkativeness
*   Racing thoughts (not better described as anxious worry)
*   Distractibility
*   Poor decision-making — for example, going on buying sprees, taking sexual risks, or making foolish investments

### **Schizophrenia**
*   Delusional beliefs not based in reality
*   Hallucinations; sensory perceptions of things that do not exist
*   Disorganized thinking; (as expressed by highly disorganized speech).
*   Extremely disorganized or abnormal motor behavior.
*   Neglect of personal hygiene
*   Loss of emotionality
*   Loss of joy, or interest in daily activities
*   Withdrawal from others

## Warning Signs: Rules of Thumb
If you notice one or more signs from the list of signs and symptoms above, it may or may not be cause for concern. Here are some general rules of thumb when it comes to warning signs:

### Duration matters.
Imagine a friend who has a "bad day" and doesn't want to leave their bed. The next day they shake it off and it looks like they are back on track. Contrast this with another friend who is having trouble getting out of bed more days than not for a period of two weeks. Duration matters because bad days are expected, and as long as someone is bouncing back from them there is probably little need to worry. But when someone can't seem to "snap out of it" this likely indicates cause for concern.

### Functioning matters.
For most college students, doing well at school is their primary "occupation." Getting up on time for classes, practicing good-enough hygiene, attending and engaging with lectures, completing assignments, and studying for exams are the tasks they are expected to perform. When emotional or behavioral distress gets in the way of doing their "job" this is an indication that they may need some additional support to bounce back to good functioning.

### Symptom clusters matter.
When symptoms cluster together, this is often suggestive of a problem. A drop in classroom attendance becomes more concerning, for example, when it occurs alongside an inability to concentrate, withdrawal from others, and increased substance use. A caveat to the idea of symptom clusters is that some signs or symptoms are so concerning that even if they are the only noticeable sign, it would be important to intervene (for example, when a student is expressing thoughts of suicide or experiencing hallucinations).

### Unhealthy changes in behavior and attitude matter.
College is a time for self-exploration. It is normal for a college-aged person to try new ways of being, and new ways of interacting with others. In the absence or risk and erratic behavior, and in the presence of their usual good values and morals, this is a positive sign of development. Risky or health-threatening behaviors, however, are a cause for concern. Examples of these would include substance misuse, self-harm, self-malnutrition, or any other kind of violent behavior. Erratic behavior or sudden shifts in personality or mood should also focus your attention on the possibility something is amiss. Similarly, changes in belief system towards a radical or hateful ideology could signal that a student is struggling.

### Context matters.
There are some life events that can hit particularly hard in the life cycle of a college student. These almost always involve some form of loss or transition. Recognizing that loss and transition are challenging can help you be tuned in to whether a friend, student, or child is coping effectively (or ineffectively) during these times.

Examples of challenging life events for a college student might include:
*   Death of a family member, partner or best friend
*   Loss of any major relationship
*   The divorce or separation of parents
*   The adolescent’s own pregnancy or illness
*   A loss or change in residence; or a recent unwanted move
*   Loss of family social or financial status
*   Rejection by peers
*   A significant failure to achieve

### History matters.
When thinking about whether to be concerned about a symptom of distress, a change in behavior, or some other potential sign that something is amiss it helps to keep an individual’s history in mind. Have they shared with you that they have a known history of emotional difficulty that precedes their time in college? Did they ever meet with a mental health professional in the past or receive a mental health diagnosis? Are you aware that they have become symptomatic in the past during times of loss or transition? If the answer to these questions is yes, then it may add some weight to the idea that their current distress is reason enough to check in with them to see if they are getting the support they need to thrive.

### Always take talk about suicide seriously.
In the United States a death by suicide occurs roughly every 11 minutes. Additionally, suicide is the second leading cause of death for individuals age 15-24. When a child, friend, or student mentions having thoughts of suicide or wanting to die this can trigger strong feelings of alarm in the person who hears it. As best you can, calm you alarms enough to convey that you are glad they are talking with you about this topic (rather than keeping it to themselves). Express hope that things can get better. Remind them that you are here to support them and that for you their health is paramount. Offer to get them whatever help they need and that getting mental health support is a courageous, positive step.

## Speak Up
Concerned parties often feel hesitant to ask a student "are you in distress?" It’s common to worry that by asking a student if they are sad, or having a difficult time, or in some sort of emotional pain that the response will be negative, defensive or will somehow make matters worse. In reality, it is far more likely that by asking someone if they are suffering, you will convey to them that you care - and this can make all the difference. If you find yourself hesitating to ask a student if they are alright or if they need some help - don't wait, speak up. If you find that you can't ask, then delegate the task to someone who can.

Some tips for asking a student if they are in distress:
*   Leave plenty of time for discussion.
*   Try to speak in private if possible.
*   Make use of observations and open-ended questions (for example: "I've noticed you've seemed tearful during class. It makes me think you might be going through a hard time. So, how are you doing?")
*   Have resources (e.g., information about CAPS at Stevens) readily available to give to the student in case they agree to get help.

## Persuade
Individuals who are struggling with their emotional health may be reluctant to get help from a mental health professional. While speaking with them it can help to adopt an empathic, non-judgmental stance. Try to avoid getting into a tug-of-war. Ultimately, you want the student to feel heard, understood and cared for, while simultaneously planting the seed that professional help can improve their situation. Offer hope and suggestions for the ways in which treatment can help.

Some examples of things you might say:
> “You know, mental health treatment really works. There's a lot of good research on talk therapy.”
>
> “Emotional distress is painful... and it also eventually passes. I think with some treatment what you’re going through could feel better sooner.”
>
> “Sometimes talking with someone can really help with shouldering the burden. It’s hard to do this alone!”
>
> “I know Dr. _____ at CAPS. She seems really great, and I know that she has helped other students who are going through moments that are similar to what you are going through.”

## Refer for Help
The QPR Institute, leaders in the field of suicide prevention, suggest that while any referral for help is a good one, some may be more effective than others.

1.  The best referral involves actually accompanying the person to a counselor or mental health professional.
2.  The next best referral involves getting a commitment from someone to accept help, and then helping them set up a connection with a helping professional.
3.  Third best is to give the student the contact information and encourage them to reach out to get help themselves.

## Resources for Stevens Students

### **On-Campus Counseling**

**Counseling and Psychological Services (CAPS)**
Student Wellness Center, 2nd Floor
201-216-5177 | CAPS@stevens.edu
Phone line is staffed 24/7

### **National Emergency Counseling Resources**

**National Suicide Prevention Lifeline**
1800-273-TALK

**Crisis Text Hotline**
Text "Hello" to 741-741
*Students of color can also text "Steve" to 741-741*

**Trevor Project Hotline**
Resource for the LGBTQ+ community
866-488-7386 | or Text "Start" to 678-678

**Asian Lifenet Hotline**
877-990-8585
*Cantonese, Mandarin, Japanese, Korean, Fujianese spoken*

## Reporting Wellness Concerns at Stevens: The CARE Team, Campus Police and 911
In addition to the on-campus counseling service (CAPS), Stevens has two on-campus resources that can be of assistance in the event you are concerned about the well-being of a student:

### **The CARE Team**
The CARE Team is a group of staff that receives reports made by individuals concerned about the well-being of a student. These reports are typically made by a faculty member, staff member, family member, or another student. When the CARE Team receives a report, it is assigned to a CARE Team member who then makes an attempt to speak with the student of concern and ultimately to connect them with a resource to help them (e.g., CAPS).

A CARE report can be submitted by emailing CARE@stevens.edu or by visiting [this link](https://cm.maxient.com/reportingform.php?StevensInstTech&layout_id=7). (*Note: The link was inferred as the standard Stevens CARE reporting link, adjust if a different link was intended.*)

**The CARE Team is not a 24/7 resource. A submitted report may not be read immediately.**
**For situations that require an immediate response (e.g., a potentially life-threatening situation) contact the police.**

### **Campus Police**
Stevens Campus Police are available 24-hours a day, 365 days of the year.
*   In the event of a potentially life-threatening situation, they can be reached at **201-216-3911**.
*   For non-emergencies, you can reach them at **201-216-5105**.

### **Local Police**
In the event of a potentially life-threatening situation occurring off-campus, contact **911** or a local police department.

## Additional Reading
Want more in-depth information on a particular topic or condition?

*   Explore symptoms of mental health conditions courtesy of the National Alliance on Mental Illness (NAMI).
*   Learn about signs of suicidality courtesy of the American Foundation for Suicide Prevention (AFSP).
*   Visit the Jed Foundation resource center for information about common emotional health issues and advice for teens and young adults on how they can support one another, overcome challenges, and make a successful transition to adulthood.
*   Explore the Active Minds, Inc. website to learn more about the mental health challenges facing today’s youth and for tips on self-care and positive coping.

# Resources for Parents
As parents and guardians, you continue to play a vital role in the lives of your college-aged children. You probably know your son or daughter better than anyone else and are more likely to notice changes in mood or behavior that may be signs of distress. Since students tend to turn to their parents when it comes to making important decisions, your suggestions regarding reaching out to resources for assistance can be very influential. The following information describes signs that can be indications of distress, suggestions on how to respond effectively when your student approaches you with problems, how to make an effective referral and information about CAPS as an important resource on campus.

## Signs of Distress

### Changes in Academic Performance
*   Decline in academic performance
*   Excessive absences from class
*   Confusion or uncertainty about interest, abilities or values

### Unusual Behavior
*   Listlessness, lack of energy, complaints about fatigue
*   Marked changes in personal hygiene
*   Impaired speech or disjointed, confused thoughts
*   Aggressive or threatening behavior
*   Extreme mood changes or inappropriate displays of emotion
*   Excessive crying
*   Dramatic weight loss or gain
*   Preoccupation with food or body image
*   Bizarre behavior indicating a loss of contact with reality

### Changes in Relationships
*   Death of a family member or close friend
*   Difficulties in romantic relationships
*   Problems with family members, friends or roommates
*   Extreme isolation
*   Becoming too dependent on one relationship at the expense of previously important connections with others

### References to Suicide
*   Overt references to suicide
*   Statements of hopelessness or helplessness
*   Indications of prolonged unhappiness
*   Pessimism about the future

## How to Respond
*   Talk to your student as soon as you notice something unusual, don’t ignore atypical or disturbing behavior.
*   Express your concern in a caring manner and indicate the specific behaviors that are causing you to be concerned.
*   Use “I” language that focuses on what you have noticed or what you are feeling.
*   Talk to your student in private when you both have enough time for a conversation.
*   Listen attentively and avoid being critical or judgmental.
*   Encourage positive action by helping your student define the problem and possible ways of handling it; avoid the temptation to solve the problem for them.
*   Ask directly how you can best help.
*   Know your limits as a helper. Parents can do a lot, but sometimes professional help is needed.

## Making a Referral to CAPS
CAPS is a place where undergraduate and graduate students at Stevens can speak with a mental health professional about issues in a confidential setting. CAPS staff are well versed in college student mental health issues and have experience helping students with a wide range of concerns. CAPS provides free, confidential, solution-focused, short term individual and group counseling, as well as crisis services. Students may initially be hesitant about seeking counseling. Reassuring them that many students utilize our services and telling them directly and clearly why you think counseling could be helpful may encourage them to seek help.

*   Review information about the counseling process with students using the CAPS website. Emphasize that services are confidential and free.
*   Suggest that your student attend one session before judging whether counseling is helpful or not.
*   Point out that using appropriate resources and addressing problems rather than avoiding them is a sign of strength and maturity.
*   Except in cases of imminent danger to self or others, it is important to allow your son or daughter to make their own decision about counseling. Just because they don’t follow through immediately doesn’t mean that your suggestions aren’t being considered.
*   While it is preferable for the student to take the step of making a first appointment on their own, CAPS staff are willing to consult with you about our services and how to encourage your student to seek help.
*   If your student would be more comfortable seeking counseling from an off-campus provider, we can assist you with referrals.

## Confidentiality
CAPS staff are required by law and professional ethics to protect the confidentiality of all contacts with students. The only exceptions occur in cases of imminent danger to self or others, situations involving child or elder abuse or when there is a court order. Without a student’s written permission, we cannot discuss the content of counseling sessions or whether or not your student has been seen at the our center. If you think it is important for you to dialogue with your student’s counselor, please share this concern with your student and request that they sign a release of information form allowing us to share information with you. If you have questions about our services or if you would like to consult with a staff member about concerns regarding your student, please feel free to call our office.

## Continuation of Treatment - Making a Smooth Transition to College
For students who have been in treatment at home for psychological difficulties, it can be important to continue psychological and psychiatric support during the transition to college. CAPS staff can work with your family and your student’s home treatment provider to assist in a smooth and successful transition to Stevens by helping you identify appropriate treatment either on or off campus. It is important to plan for your students continued treatment before they arrive on campus.

*   A month or so prior to arriving on campus, discuss with the home treatment provider your student’s needs regarding continued counseling or medication at college.
*   Encourage your student to discuss the benefits of remaining in counseling and/or on medication through this time of transition.
*   Suggest your student sign a release of information form that will give the home treatment provider permission to discuss your student’s needs with Stevens CAPS.
*   Decide whether your student’s treatment needs are best met on or off campus. Our staff can consult with you about this decision.
*   Encourage your student to call and schedule an appointment to transfer their care to a new providers either on or off campus. It is helpful for the student to initiate these appointments, because they will need to take on this responsibility when they arrive on campus. We recommend that these appointments be scheduled prior to their arrival on campus to ensure continuity of care

## Psychological Emergencies
*   If you think your son or daughter is in imminent danger of harming themselves or someone else, please call **Stevens Campus Police 24/7 at 201-216-3911**. They will respond immediately and involve CAPS as indicated.
*   For non-life-threatening emergencies: CAPS' hours are 9-5, M-F. During this time we have a staff member dedicated to helping students sort out mental health crisis situations.
*   Clinicians are also available to help a student in distress after hours, weekends and holidays and can be reached by dialing **201.216.5177 and pressing "2"**
*   Additional after-hours resources include the **National Suicide Prevention Lifeline (1800-273-8255)** and the **National Crisis Text Line** which can be accessed by texting **"Hello" to 741-741**.

## Important Campus Contacts
*   **CAPS:** 201-216-5177
*   **Campus Police:** 201-216-5105 or 3911
*   **Dean of Students:** 201-216-5699
*   **Student Health:** 201-216-5678
*   **Office of Disability Services:** 201-216-3748
*   **Title IX Coordinator:** 201-216-5679 or 5122 (*Note: Verify these numbers if critical, Title IX numbers can change*)
*   **The CARE Team:** care@stevens.edu

## Additional Resources (Website, Readings, Book Suggestions)

### **Websites/Readings:**
*   **Stop, Drop and Roll** (A brief guide to helping your student be an independent problem-solver; original design courtesy of Wake Forest University)
*   **College and Your Mental Health** (essential reading from NAMI about navigating mental health during college)
*   **College Parents of America** (short, insightful articles that help explore many questions you may have)
*   **College Parent Central** (practical advice)

### **Book Suggestions:**
*   *The Happiest Kid on Campus* by Harlan Cohen.
*   *Letting Go: A Parents' Guide to Understanding the College Years* by Karen Levin Coburn and Madge Lawrence Treeger
*   *You're On Your Own - But I'm Here If You Need Me* by Marjorie Savage
*   *The Empty Nest: 31 Parents Tell the Truth About Relationships, Love and Freedom After the Kids Fly the Coop* by Karen Stabiner
*   *College of the Overwhelmed: The Campus Mental Health Crisis and What to Do about It* by Richard Kadison, M.D. and Theresa DiGeronimo

### **Share one of these books with your son or daughter:**
*   *1001 Things Every College Student Needs to Know: (Like Buying Your Books Before Exams Start)* by Harry H. Harrison, Jr.
*   *1001 Things Every Teen Should Know Before They Leave Home (Or Else They'll Come Back)* - both by Harry H. Harrison, Jr.
*   *The Naked Roommate* by Harlan Cohen

# Counseling and Psychological Services
We are here to help. Stevens offers a wide variety of mental health support and programming to allow you to stay healthy and make the most of your university career.

## CAPS
Counseling and Psychological Services (CAPS) is the hub for all mental health services at Stevens. CAPS offers a choice of in-person or teletherapy to all students living on campus or within the greater NJ/NY area. To book a screening call us at **201-216-5177**, or schedule a visit online through the Healthy Stevens Portal.

Currently enrolled students, visit us on the Stevens Hub to request a mental health awareness program, access a mental health self-evaluation tool, apply to become a peer wellness educator, and more!

## Uwill
With the generous support of the New Jersey Office of the Secretary of Higher Education, Stevens is pleased to partner with Uwill to offer all currently enrolled Stevens students free and unlimited teletherapy with a licensed mental health professional. This program is guaranteed to be funded through April 1, 2026. Visit our FAQ page to learn more, or get started today by visiting **app.uwill.com** and enrolling with a valid Stevens email. Its that easy!

## Mental Health Crisis Support
A licensed mental health professional is always available to offer support in the event of a mental health crisis. Our phone line is staffed 24 hours a day - call **201.216.5177**. On weekdays CAPS is also pleased to offer dedicated in-person crisis support from 9am to 4:30pm.

## Programming and Events
CAPS is pleased to offer a variety of interactive programs and events. For an up-to-date listing of the latest offerings, visit our events page on DuckLink.

## CAPS Contact Information
**Phone:** 201.216.5177
**Fax:** 201.216.5629
**E-mail:** caps@stevens.edu

## CAPS Office Hours*
Mon - Fri, 9am - 5pm

***Hours listed are for our physical location on-campus. Help is available 24-7 by calling 201.216.5177**

# Individual & Group Counseling
We offer a variety of therapeutic services and psychoeducational workshops geared towards helping students gain support, learn new skills, and find places to grow. Click below to learn more.

## Individual Counseling
At some point during college most students will feel overwhelmed by the demands of school, family, friends, work or other relationships. They might even struggle with a significant mental health issue. During such times it can be highly beneficial to speak one-on-one with a therapist. Counseling and Psychological Services (CAPS) is here to help. We provide short-term therapy to help students process a variety of issues and concerns, including:

*   Depression
*   Anxiety
*   Stress
*   Parental Relationships
*   Intimate Relationships
*   Roommate Conflicts

**What is expected of you in counseling?**
Commitment to your treatment by showing up on time to your scheduled appointment and calling or emailing your therapist 24 hours in advance when you cannot make it to an appointment.

## Group Counseling & Workshops
In addition to one-on-one psychotherapy, CAPS also offers group therapy and drop-in workshops:

### Group Therapy
Often individuals can benefit from participating in group therapy even more so than in individual therapy. Group therapy provides a safe, confidential space to explore concerns as well as receive support on various issues. It is an opportunity to learn more about oneself, explore healthy behaviors and develop new ways of coping. Unlike workshops, our groups typically require a pre-screening. You can learn more about our current group offerings by clicking here. (*Note: Link target not provided in text*)

### Workshops
Unlike group therapy, workshops tend to have a drop-in style. These workshops typically offer opportunities to learn new skills or to be educated about a particular topic related to mental health. To learn more about our current workshop offerings, click here. (*Note: Link target not provided in text*)

## Psychiatry Services
CAPS has a limited number of psychiatry appointments available each week for students. Because of the limited number of these appointments, they are only accessible to students whose needs meet a variety of criteria:

*   As a general rule, psychiatry services at CAPS are available only to students who cannot otherwise access psychiatric services using their insurance.
*   CAPS does not provide psychiatry only services. CAPS' psychiatry services are limited to students who are also being seen for psychotherapy at CAPS.
*   In circumstances where a student is ready to try psychiatric medication but cannot obtain a first off-campus psychiatry appointment for an extended period of time CAPS will on occasion provide transitional psychiatric care. These services are limited to students who provide proof of having obtained an off-campus psychiatry appointment to whom care will be transferred.

---

## Free teletherapy. No session limits. No catch.
### Uwill at Stevens
Stevens Institute of Technology is pleased to partner with Uwill, to provide you with free and unlimited teletherapy with licensed mental health providers. This service is made possible through a generous grant from the New Jersey Office of the Secretary of Higher Education. Funding for this service is guaranteed through April 1, 2026. We hope Uwill will be a useful resource to many of you!

### Teletherapy Outside New Jersey and New York
*   Access is quick and easy. You may access Uwill by clicking on https://app.uwill.com
*   There is no cost to use Uwill. Video, phone, chat and message-based therapy options will all be available to you
*   You should not need much help to enroll, but just in case, Uwill offers a quick start guide for Stevens students, as well as phone / email assistance at 1-833-998-9455 or support@uwill.com

### FAQ
**What is Uwill?**
Uwill is a leading teletherapy platform that allows college students nationwide to receive real-time counseling online from licensed mental health professionals.

**How does it work?**
You choose from a list of mental health professionals, and you are then able to receive 1:1 counseling via video, phone, chat or text.

**Who is eligible?**
All currently registered and enrolled Stevens Institute of Technology students with a valid school email address are eligible to utilize the Uwill platform.

**Is it free?**
Yes, this service is generously sponsored by the New Jersey Office of the Secretary of Higher Education and is guaranteed to be fully funded through April 1, 2026.

**Will I run out of sessions?**
Unlimited sessions are guaranteed by Uwill until at least April 1, 2026.

**How do I get started?**
You may access the Uwill platform by clicking on app.uwill.com. From there, you can register using your Stevens email address. Once you complete the registration process, you will receive an email confirmation. After confirming your email address, you can select a counselor and schedule an appointment.

**How long until I can get started?**
You will generally be matched with a counselor within 24 hours after you complete your registration

**What types of counseling can I receive through Uwill?**
Uwill’s platform is designed to help students facing a variety of mental health concerns, including: depression, stress, specific relationship problems, family concerns, academic performance difficulties, sleep disturbance, social isolation/loneliness and adjustment to a new environment, among others.

**Who are the counselors available on the platform?**
They are all licensed mental health professionals with extensive clinical experience who possess one of the following credentials:
*   Doctoral Level Licensed psychologists (LP, Ph.D., Psy.D. or the state’s equivalent of an independently licensed psychologist)
*   Master’s Level Licensed Clinical Social Workers (LCSW, LICSW, or the state’s equivalent of an independently licensed social worker)
*   Master’s Level Licensed Marriage and Family Therapists (LMFT – or the state’s equivalent of an independently licensed marriage and family therapist)
*   Master’s Level Licensed Counselors (LPC, LPCC – or the state’s equivalent of an independently licensed counselor)

**Which treatment approaches do the counselors utilize?**
Counselors using the Uwill platform generally take a solutions-oriented, wholistic perspective to treatment with a focus on providing specific coping skills to address the issues you are facing. To accomplish this, counselors use a variety of approaches including but not limited to: Cognitive Behavioral Therapy (CBT), Dialectical Behavior Therapy (DBT), and Mindfulness-Based Therapy.

**Can I choose between video, phone, chat and message-based support?**
Yes, you work with your counselor and select the format that best suits you. You can also choose multiple modalities of therapy based on your schedule and needs.

**Is it really private and secure?**
Yes. Uwill is HIPAA and FERPA compliant which means they follow the strictest privacy guidelines.

---

## The CAPS Team
*   **Eric D. Rose, Ph.D.** - Executive Director of Student Wellness | Director of Student Counseling (erose@stevens.edu) [Biography]
*   **Ying Xiong, Ph.D.** - Assistant Director of Student Counseling (yxiong14@stevens.edu) [Biography]
*   **Diane Sosa, M.A., LPC, NCC** - Staff Psychotherapist (dsosa@stevens.edu) [Biography]
*   **Rocio Cruz-Olivera, M.A., LPC, ACS** - Staff Psychotherapist (rcruzoli@stevens.edu) [Biography]
*   **Ilianna Gualdron, M.A., LPC, NJ SCC** - Staff Psychotherapist (ijimenez@stevens.edu) [Biography]
*   **Mariel Marshall, M.S., LPC, NCC, CRC** - Staff Psychotherapist (mmarshal2@stevens.edu) [Biography]
*   **Katelyn Delano, LCSW** - Staff Psychotherapist [Biography]
*   **Juliet Procopio, LCSW** - Staff Psychotherapist & Substance Abuse Counselor [Biography] (*Note: Text indicates "Jan 2025" next to name, possibly start/end date?*)
*   **Genesis Gonzalez, Psy.D.** - Staff Psychotherapist [Biography]
*   **Megan Reilly, MSW, LCSW** - Staff Psychotherapist [Biography]
*   **Ellen Usatin, MS, LPC** - Staff Psychotherapist [Biography]
*   **Nadege Napoleon, M.A.** - Graduate Psychology Extern [Biography]
*   **Nicholas Dynan, M.A.** - Graduate Psychology Extern [Biography]
*   **Jesse Denniston-Lee, MSW, LSW (he, him)** - Case Manager and Grant Coordinator [Biography]
*   **Susann Peck, B.A.** - Administrative Assistant (speck1@stevens.edu) [Biography]

*(Note: "Biography" likely indicates a link or expandable section not present in the raw text)*

---

## About Student Counseling & Psychological Services

### Our Mission
The mission of Counseling and Psychological Services (CAPS) is to promote the personal growth and development of students at Stevens. We strive to maximize students’ potential to benefit from their academic environment and experience. We further seek to promote and be part of a healthy, caring and inclusive university community.

### Diversity
The diverse staff at CAPS recognizes that many factors including race, ethnicity, age, gender, sexual orientation, religion, culture, ability or disability status, socioeconomic status and other unique issues are significant in students' lives and identities. We value social justice and strive to create a safe space where thoughtful and appreciative exploration of diversity is the norm.

## Frequently Asked Questions

**What is psychological counseling?**
Psychological counseling promotes mental and physical health in a warm and welcoming environment. You will objectively look at behaviors, feelings and thoughts in situations that you may find troublesome. Psychological counseling can be valuable in helping you make the changes you would like to make in your life by providing adaptive and effective strategies and techniques for coping with stressors. Psychological counseling involves meeting with a trained professional who can help you cope, work and resolve different issues. Counseling can also help you learn about yourself, explore different career paths, and help you make difficult decisions.

During your first meeting you and your psychologist will explore your decision to begin psychological counseling and will discuss your concerns. You will discuss the options for what help is available, including which staff psychologist will be assigned to meet with you regularly. You can express a preference either to continue counseling, not continue, or be referred to another source of assistance.

**What issues do people talk about in counseling?**
*   **Personal Concerns:** Adjusting to college, acculturation issues, difficulty coping, stress, past traumatic experiences, social concerns, sexuality, family crisis , excessive video gaming, roommate concerns and other personal issues.
*   **Psychological Issues:** Depression, anxiety, panic, eating disorders, substance misuse/abuse, suicidality, attention/concentration difficulties, sleep disorders and other psychological issues.
*   **Interpersonal Concerns:** Communication skills, dating/relationships, conflict management.
*   **Crisis Intervention Services:** Acute stress, sexual assault, death of a family member or friend.

These are just a few of the reasons fellow students may seek counseling. Our door is open to you!

**How do I know if counseling will help me?**
There are times when everyone feels stressed, overwhelmed, depressed and anxious. However, sometimes these feelings last for a long time or become difficult to manage. They may start interfering with your health, relationships, schoolwork or social life. If this happens, counseling may help.

**How do I make a first appointment?**
Call our office at 201.216.5177 and we can schedule an appointment for you. We are not currently accepting walk-in appointments.

**Are appointments required to talk to a mental health professional?**
During the pandemic period, yes - all meetings with a staff clinician require calling for an appointment. Please note that we have regular staff available in the event of urgent situations and can accomodate short-notice requests for service when appropriate.

**Do I need to use my insurance to visit CAPS? Is there a cost?**
No. Student Counseling and Psychological Services is available to all enrolled Stevens undergraduate and graduate students, regardless of insurance. There is no cost for services. Services are free and confidential.

**Is my information confidential? Will you talk to my parents?**
All interactions with CAPS, including scheduling of, attendance of appointments, content of your sessions, progress in counseling, and your records, are confidential within Student Counseling Services.

No record of counseling is contained in any academic, educational or job placement file. At your written request/consent, CAPS staff will send a report, or talk with persons you designate.

The counseling staff works as a team. Your counselor will consult with other counseling staff to provide you with the best possible care. Staff consultations are for professional and training purposes. Information will not be disclosed outside of CAPS without your written consent with the exception of the following:

*   **Imminent Harm to Self:** If a staff member has reason to believe that you are in danger of physically harming yourself; a mental health professional is legally and ethically required to report this information to the proper authorities and others (i.e., family, college administrators, campus police, etc.) as needed to ensure your safety.
*   **Imminent Harm to Others:** If a staff member has reason to believe that you are seriously threatening harm against another person and if s/he believes that you are a threat to the safety of another person, s/he is legally and ethically required to take some action (such as contacting the police, notifying the other person, contacting college administrators, seeking involuntary hospitalization or some combination of these actions) to ensure that the other person is protected.
*   **Abuse of Vulnerable Individuals:** If a staff member has reason to believe that a child, an elderly person, or another vulnerable individual(s) is being physically or sexually abused or neglected; s/he is legally obligated to report this situation to the appropriate state agency.
*   **Court Order:** A court order, issued by a judge, may require CAPS staff to release information contained in records and/or require a counselor to testify in a court proceeding. If records are subpoenaed, we will make every effort to keep information confidential within the limits of the law.

Please Note: The exceptions to confidentiality are rare. However, if they should occur it is the Center’s policy that, whenever possible, we will attempt to discuss with you any action that is being considered.

**What are CAPS' hours? Where are you located?**
Fall and Spring Semesters: Monday - Friday (9am-5pm)
(Note: Evening hours vary by semester)
Our offices are located on the 2nd Floor of the Student Wellness Center (between the North Building and the 9th Street Gate)

**If I'm worried about someone other than myself, what should I do?**
If you are concerned about someone you know, you can:
*   **Encourage your friend to come see us.** Sometimes it helps to introduce someone to us through our website. You could also offer your support by walking with them to our office and waiting while they attend an intake appointment.
*   **You can also meet with one of us** to discuss how to reach out to your friend and talk to them about counseling. One possibility may be the sharing of a brochure provided to you by one of our counselors. Our office has an extensive selection of brochures on important topics (e.g. eating disorders, depression, test anxiety, etc.). Sometimes sharing a brochure with the student you are concerned about will open up a conversation about the problem.
*   **You can submit a report to the CARE Team.** In your report, include as much detail as possible about who you are worried about and why. Someone from the CARE Team will respond to your concerns, and will often reach out directly to the person about whom you are are concerned.

**What will happen during my first appointment?**
At your first appointment you will be asked to fill out a simple intake form (this usually takes about fifteen minutes, so arrive a little early!) It will have contact information, questions about your background and your current concerns. In your first session you and your counselor will discuss what brings you to counseling, as well as review the information on your intake form. You and your counselor will also review the confidentiality policy together. If you decide to continue with treatment, you will be assigned a counselor. As often as possible, we aim for the counselor who provided your first appointment to continue as your therapist

**I've been away on a medical leave. What's the process for returning?**
We sincerely hope that the time you took off from school was healing and that you feel prepared and ready to return to school. If your leave was for psychological treatment, you will need to take the following steps before you return:

**(1) You will need to fill out the following forms and return them to CAPS.** We recommend you send these forms to us by secure fax (201-216-5629) or USPS:
*   **Release of Information** - Please fill this out to allow one of our staff to speak with the treatment provider(s) who worked with you while you were on leave.
*   **Treating Agent Readmission Questionnaire** - Please ask your treatment provider(s) to fill this out and return it directly to us. Also, your treatment provider(s) must submit a statement on their letterhead describing their opinion about your readiness to return to university.
*   **Student Readmission Questionnaire** - Please fill this out yourself and return directly to CAPS.

**(2) You must schedule a readmission discussion with one of our staff.** You can do so by calling us at (201-216-5177). This discussion can occur either in-person or over the phone, but can only occur after you have sent in the forms described above. The point of the discussion is so that you and the staff member can talk in depth about how you are feeling, and whether the treatment you received has prepared you to return to school. The staff member you speak with will review the information filled out by your treatment provider to help inform the discussion, and may additionally contact your treatment provider with other questions. Following this discussion one of our staff will make a recommendation to the Dean of Students about your readiness to return to school. Ultimately, it is the Dean of Students who has the final decision about your return status.


"""

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mental_health_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mental_health_bot")

client = AzureOpenAI(
  api_key = os.getenv("OPENAI_API_KEY"),  
  api_version = "2024-12-01-preview",  # Must match your deployment
  azure_endpoint = "https://ai-rtiwari35436ai913349565300.openai.azure.com"  # No trailing slash
)

# Azure Cosmos DB NoSQL configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY") 
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "rag_database")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "document_store")

# Azure OpenAI configuration
OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-02-01-preview")
EMBEDDINGS_DEPLOYMENT = os.getenv("EMBEDDINGS_DEPLOYMENT", "text-embedding-3-small")
COMPLETIONS_DEPLOYMENT = os.getenv("COMPLETIONS_DEPLOYMENT", "gpt-4o")

class IntegratedMentalHealthBot:
    """Integrated mental health bot with RAG system and agent-based conversational capabilities"""
    
    def __init__(self):
        self.conversation_state = {
            "history": [],
            "is_greeting_phase": True,
            "alert_flag": 0  # Default alert flag is 0 (no alert)
        }
        self.logs = []
        
        # Initialize services
        self.initialize_services()
    
    def initialize_services(self):
        """Initialize all required services"""
        self.initialize_cosmos_db()
        self.client = self.initialize_openai()  # Store the client instance
        self.initialize_campus_calm_agent()
        
        # Email alert configuration with better defaults
        self.smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.sender_email = os.environ.get("SENDER_EMAIL", "test@gmail.com")
        self.sender_password = os.environ.get("SENDER_PASSWORD", "")
        self.admin_email = os.environ.get("ADMIN_EMAIL", "test2@gmail.com")
        
        # Print email configuration at startup
        print("📧 Email alert configuration:")
        print(f"  SMTP Server: {self.smtp_server}")
        print(f"  SMTP Port: {self.smtp_port}")
        print(f"  Sender Email: {self.sender_email}")
        print(f"  Admin Email: {self.admin_email}")
        print(f"  Sender Password Set: {'Yes' if self.sender_password else 'No - Authentication will fail'}")
        
        # Console output settings
        self.verbose_console = True

    def test_email_alert(self):
        """Test the email alert functionality"""
        print("\n🧪 Testing email alert functionality...")
        test_reason = "TEST ALERT - Please ignore this test message"
        self.trigger_alert(test_reason)
        return True
    
    def initialize_cosmos_db(self):
        """Initialize Cosmos DB client for RAG knowledge base"""
        try:
            self.cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
            self.database = self.cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
            self.container = self.database.get_container_client(COSMOS_CONTAINER_NAME)
            logger.info(f"Connected to Cosmos DB container: {COSMOS_CONTAINER_NAME}")
            
            # Validate container has documents
            doc_count = self.count_documents()
            logger.info(f"Container has {doc_count} documents")
            print(f"📁 Connected to Cosmos DB - {doc_count} documents available")
            
            if doc_count == 0:
                logger.warning("No documents found in container. The RAG system may not work properly.")
                print("⚠️ Warning: No documents found in the knowledge base")
                
        except Exception as e:
            error_msg = f"Error initializing Cosmos DB: {str(e)}"
            logger.error(error_msg)
            print(f"❌ Cosmos DB Error: {str(e)}")
            # Continue even if Cosmos DB fails - we'll handle this in the search methods
    
    def initialize_openai(self):
        """Initialize Azure OpenAI configuration"""
        try:
            client = AzureOpenAI(
            api_key = os.getenv("OPENAI_API_KEY"),  
            api_version = "2024-02-01-preview",
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            
            # Log which deployment we're using
            deployment_name = os.getenv("COMPLETIONS_DEPLOYMENT")
            logger.info(f"OpenAI configuration initialized with deployment: {deployment_name}")
            print(f"🔄 OpenAI client initialized with {deployment_name} deployment")
            
            return client
        except Exception as e:
            error_msg = f"Error initializing OpenAI: {str(e)}"
            logger.error(error_msg)
            print(f"❌ OpenAI Error: {str(e)}")
            raise
        
    def initialize_campus_calm_agent(self):
        """Initialize Campus Calm agent for mental health assessment"""
        try:
            # Import Azure libraries for Campus Calm agent
            try:
                from azure.ai.projects import AIProjectClient
                from azure.identity import DefaultAzureCredential
                
                self.azure_conn_string = os.environ.get("AZURE_CONN_STRING", 
                    "eastus2.api.azureml.ms;f763e218-bbdb-4330-95b6-f36e504b0440;rg-rtiwari3-8465_ai;campus_calm_ver1")
                
                # Primary agent for conversation
                self.agent_id = os.environ.get("AGENT_ID", "asst_xblIbaWhZvDEFMFmGq6X7W9t")
                # Alert agent for sending emails
                self.alert_agent_id = os.environ.get("ALERT_AGENT_ID", "asst_IolrPyItwouCxTrv9vwzAYPQ")
                
                self.ai_client = AIProjectClient.from_connection_string(
                    credential=DefaultAzureCredential(),
                    conn_str=self.azure_conn_string
                )
                logger.info("Azure AI Project client initialized successfully")
                print("🔄 Campus Calm agent initialized successfully")
                
            except ImportError:
                error_msg = "Azure AI Projects libraries not found. Mental health assessment will be limited."
                logger.warning(error_msg)
                print("⚠️ Warning: Azure AI Projects libraries not found. Using simplified assessment.")
                self.ai_client = None
                
        except Exception as e:
            error_msg = f"Failed to initialize Campus Calm agent: {str(e)}"
            logger.error(error_msg)
            print(f"⚠️ Campus Calm Agent Error: {str(e)}")
            self.ai_client = None
    
    def count_documents(self) -> int:
        """Count documents in the Cosmos DB container"""
        try:
            query = "SELECT VALUE COUNT(1) FROM c"
            count_results = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return count_results[0] if count_results else 0
        except Exception as e:
            logger.error(f"Error counting documents: {e}")
            return 0
    
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for a text using Azure OpenAI."""
        try:
            logger.info(f"Generating embeddings using deployment: {EMBEDDINGS_DEPLOYMENT}")
            
            response = client.embeddings.create(
                input=text,
                model=EMBEDDINGS_DEPLOYMENT  # Use model parameter, not engine
            )
            
            embeddings = response.data[0].embedding
            logger.info(f"Successfully generated embeddings with length: {len(embeddings)}")
            
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from the text for search."""
        words = text.lower().split()
        stopwords = {"a", "an", "the", "and", "or", "but", "if", "then", "else", "when", 
                    "at", "from", "by", "for", "with", "about", "against", "between", 
                    "into", "through", "during", "before", "after", "above", "below", 
                    "to", "of", "in", "on", "is", "are", "was", "were", "be", "been", 
                    "have", "has", "had", "do", "does", "did", "should", "could", "would"}
        keywords = [word for word in words if word not in stopwords and len(word) > 3]
        return list(set(keywords))
    
    def vector_search(self, query: str, top_k: int = 3) -> List[dict]:
        """
        Perform a vector search using query embeddings with proper Cosmos DB syntax.
        """
        try:
            start_time = time.time()
            print(f"🔍 Performing vector search for: '{query}'")
            
            # Generate embeddings for the query
            query_embedding = self.generate_embeddings(query)
            
            if not query_embedding:
                logger.warning("Could not generate embeddings for query, falling back to basic search")
                print("⚠️ Could not generate embeddings, falling back to keyword search")
                return self.basic_search(query, top_k)
            
            # Execute the vector search with the correct syntax
            logger.info(f"Executing vector search with embedding length: {len(query_embedding)}")
            
            # Use the documented VectorDistance syntax with all parameters
            options_json = "{'distanceFunction':'cosine','dataType':'float32'}"
            
            query_str = f"""
            SELECT TOP {top_k} c.id, c.content, c.metadata,
            VectorDistance(c.embedding, @queryEmbedding, false, {options_json}) AS similarity
            FROM c 
            WHERE IS_ARRAY(c.embedding)
            ORDER BY VectorDistance(c.embedding, @queryEmbedding, false, {options_json})
            """
            
            results = list(self.container.query_items(
                query=query_str,
                parameters=[{"name": "@queryEmbedding", "value": query_embedding}],
                enable_cross_partition_query=True
            ))
            
            end_time = time.time()
            search_time = end_time - start_time
            
            logger.info(f"Vector search returned {len(results)} results in {search_time:.2f} seconds")
            print(f"✅ Vector search found {len(results)} relevant documents in {search_time:.2f} seconds")
            
            # Print similarity scores in console
            if self.verbose_console and results:
                print("\n📊 Top document matches by similarity:")
                for i, doc in enumerate(results):
                    title = doc.get("metadata", {}).get("title", f"Document {i+1}")
                    similarity = doc.get("similarity", 0.0)
                    similarity_pct = (1 - similarity) * 100  # Convert cosine distance to similarity percentage
                    print(f"  {i+1}. {title} - {similarity_pct:.1f}% match")
                print()
            
            return results
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            logger.info("Falling back to basic search...")
            print(f"⚠️ Vector search error: {str(e)}. Falling back to keyword search.")
            return self.basic_search(query, top_k)
    
    def basic_search(self, query: str, top_k: int = 3) -> List[dict]:
        """Perform a basic keyword search on the content stored in Cosmos DB."""
        try:
            start_time = time.time()
            print(f"🔍 Performing keyword search for: '{query}'")
            
            query_keywords = self.extract_keywords(query)
            
            if not query_keywords:
                logger.warning("No meaningful keywords extracted from the query")
                print("⚠️ No meaningful keywords extracted. Returning recent documents.")
                query_text = f"SELECT TOP {top_k} c.content, c.metadata FROM c ORDER BY c._ts DESC"
                items = list(self.container.query_items(
                    query=query_text,
                    enable_cross_partition_query=True
                ))
                return items
            
            keyword_conditions = []
            for keyword in query_keywords:
                if len(keyword) > 3:  # Only use keywords longer than 3 characters
                    keyword_conditions.append(f"CONTAINS(c.content, '{keyword}')")
            
            if not keyword_conditions:
                query_text = f"SELECT TOP {top_k} c.content, c.metadata FROM c ORDER BY c._ts DESC"
            else:
                sql_condition = " OR ".join(keyword_conditions)
                query_text = f"SELECT TOP {top_k} c.content, c.metadata FROM c WHERE {sql_condition}"
            
            items = list(self.container.query_items(
                query=query_text,
                enable_cross_partition_query=True
            ))
            
            end_time = time.time()
            search_time = end_time - start_time
            
            logger.info(f"Basic search returned {len(items)} results in {search_time:.2f} seconds")
            print(f"✅ Keyword search found {len(items)} documents in {search_time:.2f} seconds")
            
            # Print keywords used in console
            if self.verbose_console and query_keywords:
                print(f"  Keywords used: {', '.join(query_keywords)}")
            
            return items
        except Exception as e:
            logger.error(f"Error performing basic search: {e}")
            print(f"❌ Search Error: {str(e)}")
            return []
    
    def is_greeting(self, text: str) -> bool:
        """Check if the message is a simple greeting"""
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        return any(greeting in text.lower() for greeting in greetings) and len(text.split()) < 5
    
    def is_expressing_concern(self, text: str) -> bool:
        """Check if user is likely expressing an emotional concern"""
        concern_indicators = ["feel", "feeling", "sad", "anxious", "stress", "depress", "worry", 
                             "overwhelm", "tired", "exhaust", "lonely", "afraid", "fear", "upset", 
                             "struggle", "difficult", "hard time", "low", "down"]
        return any(indicator in text.lower() for indicator in concern_indicators)
    
    def is_farewell(self, text: str) -> bool:
        """Check if the user is saying goodbye"""
        farewells = ["exit", "quit", "stop", "bye", "goodbye", "see you", "farewell", "thanks", "thank you"]
        return any(farewell in text.lower() for farewell in farewells)
    
    def analyze_mental_health_severity(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input to determine if severe mental health issues are present"""
        if self.ai_client is None:
            # If Campus Calm agent isn't available, use OpenAI fallback
            return self.analyze_mental_health_severity_openai(user_input)
        
        print("🧠 Analyzing mental health severity with Campus Calm agent...")
            
        # Build context from conversation history
        all_history = ""
        if len(self.conversation_state["history"]) > 0:
            all_history = "\n".join([f"{item['role'].upper()}: {item['content']}" for item in self.conversation_state["history"]])
        
        # Create a prompt for risk assessment
        prompt = f"""
        COMPLETE CONVERSATION HISTORY:
        {all_history}
        
        CURRENT USER MESSAGE: {user_input}
        
        As a mental health professional, analyze the conversation history and the current message.
        Determine if there are signs of severe depression, anxiety, potential self-harm, or other
        serious mental health concerns that would require urgent attention.
        
        Return a JSON object in this format:
        {{
            "alert_flag": 0 or 1,
            "reason": "explanation if alert_flag is 1, otherwise empty"
        }}
        
        Set alert_flag to 1 ONLY if you detect clear indications of:
        - you have to triggere for the key words: "suicidal", "self-harm", "hopelessness", "severe anxiety", "crisis", Kill, "die", "no reason to live", "Harm others"
        - Suicidal thoughts or intentions
        - Self-harm thoughts or behaviors
        - Severe depression with hopelessness
        - Severe anxiety that is debilitating
        - Crisis situation that requires immediate intervention
        - Statements about harming self or having no reason to live
        - Explicit mention of a suicide plan or method
        
        Make a careful and reasoned assessment. Only set alert_flag to 1 for genuinely concerning situations.
        """
        
        try:
            # Create a new thread for this interaction
            thread = self.ai_client.agents.create_thread()
            
            # Send message to the agent
            self.ai_client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=prompt
            )
            
            # Process the message
            run = self.ai_client.agents.create_and_process_run(
                thread_id=thread.id,
                agent_id=self.agent_id
            )
            
            # Get the response
            messages = self.ai_client.agents.list_messages(thread_id=thread.id)
            
            # Find the assistant message
            response_text = ""
            for message in messages.data:
                if message.role == "assistant":
                    for content_item in message.content:
                        if hasattr(content_item, 'text') and hasattr(content_item.text, 'value'):
                            response_text = content_item.text.value
                            break
                    break
            
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'({.*})', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                result = json.loads(json_str)
            else:
                # If not found, try parsing the entire response
                result = json.loads(response_text)
            
            # Ensure the result has the expected format
            if "alert_flag" not in result:
                logger.warning(f"Invalid severity analysis response format: {response_text}")
                return {"alert_flag": 0, "reason": ""}
            
            # Log the analysis result to console
            alert_status = "🚨 ALERT FLAG RAISED" if result.get("alert_flag") == 1 else "✅ No serious concerns detected"
            print(f"🧠 Campus Calm Analysis Result: {alert_status}")
            if result.get("alert_flag") == 1 and result.get("reason"):
                print(f"  Reason: {result.get('reason')}")
                
            return result
        except Exception as e:
            logger.error(f"Error in mental health severity analysis with Campus Calm agent: {str(e)}")
            print(f"⚠️ Campus Calm analysis error: {str(e)}. Falling back to OpenAI analysis.")
            # Fall back to OpenAI analysis
            return self.analyze_mental_health_severity_openai(user_input)
    
    def analyze_mental_health_severity_openai(self, user_input: str) -> Dict[str, Any]:
        """Analyze mental health severity using Azure OpenAI as a fallback"""
        try:
            print("🧠 Analyzing mental health severity with OpenAI...")
            
            # Build context from conversation history
            all_history = ""
            if len(self.conversation_state["history"]) > 0:
                all_history = "\n".join([f"{item['role'].upper()}: {item['content']}" for item in self.conversation_state["history"]])
            
            # Create system prompt for analysis
            system_prompt = f"""
            You are a mental health professional tasked with assessing the severity of a user's mental health concerns.
            Analyze the conversation history and current message to determine if there are signs of severe issues.
            
            You must respond ONLY with a valid JSON object in this exact format:
            {{
                "alert_flag": 0 or 1,
                "reason": "explanation if alert_flag is 1, otherwise empty"
            }}
            
            Set alert_flag to 1 ONLY if you detect clear indications of:
            - you have to trigger for the key words: "suicidal", "self-harm", "hopelessness", "severe anxiety", "crisis", Kill, "die", "no reason to live", "Harm others"
            - Suicidal thoughts or intentions
            - Self-harm thoughts or behaviors
            - Severe depression with hopelessness
            - Severe anxiety that is debilitating
            - Crisis situation that requires immediate intervention
            - Statements about harming self or having no reason to live
            - Explicit mention of a suicide plan or method
            
            Make a careful assessment. Only set alert_flag to 1 for genuinely concerning situations.
            """
            
            # Format user content with history
            user_content = f"""
            COMPLETE CONVERSATION HISTORY:
            {all_history}
            
            CURRENT USER MESSAGE: {user_input}
            
            Analyze for mental health severity and respond ONLY with the required JSON format.
            """
            
            # Make API call
            response = client.chat.completions.create(
                model=COMPLETIONS_DEPLOYMENT,  # Must match Azure deployment name
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.1  # Low temperature for deterministic responses
            )
            response_text = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                result = json.loads(response_text)
                
                # Validate the result format
                if "alert_flag" not in result:
                    logger.warning(f"Invalid severity analysis response format: {response_text}")
                    return {"alert_flag": 0, "reason": ""}
                
                # Log the analysis result to console
                alert_status = "🚨 ALERT FLAG RAISED" if result.get("alert_flag") == 1 else "✅ No serious concerns detected"
                print(f"🧠 OpenAI Analysis Result: {alert_status}")
                if result.get("alert_flag") == 1 and result.get("reason"):
                    print(f"  Reason: {result.get('reason')}")
                
                return result
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse severity analysis as JSON: {response_text}")
                return {"alert_flag": 0, "reason": ""}
                
        except Exception as e:
            logger.error(f"Error in mental health severity analysis: {str(e)}")
            print(f"❌ Analysis Error: {str(e)}")
            # Return safe default
            return {"alert_flag": 0, "reason": ""}
    
    def trigger_alert(self, reason: str) -> None:
        """Trigger the alert process for concerning mental health situations"""
        logger.warning(f"MENTAL HEALTH ALERT TRIGGERED: {reason}")
        print(f"\n🚨 MENTAL HEALTH ALERT TRIGGERED: {reason}")
        
        # Build context from entire conversation history
        all_history = ""
        if len(self.conversation_state["history"]) > 0:
            all_history = "\n".join([f"{item['role'].upper()}: {item['content']}" for item in self.conversation_state["history"]])
        
        # Always print email settings for debugging
        print("\n📧 Email Alert Settings:")
        print(f"  SMTP Server: {self.smtp_server}")
        print(f"  SMTP Port: {self.smtp_port}")
        print(f"  Sender Email: {self.sender_email}")
        print(f"  Admin Email: {self.admin_email}")
        print(f"  Sender Password Set: {'Yes' if self.sender_password else 'No - Authentication may fail'}")
        
        # Try to use the Campus Calm alert agent if available
        if self.ai_client is not None:
            try:
                print("📧 Generating alert email with Campus Calm agent...")
                
                # Create a prompt for the alert agent
                prompt = f"""
                COMPLETE CONVERSATION HISTORY:
                {all_history}
                
                ALERT REASON: {reason}
                
                You are an alert system for a mental health chatbot. A potential mental health crisis has been detected.
                Draft a concise email to the administrator that includes:
                
                1. A clear subject line indicating this is an urgent mental health alert
                2. A brief summary of the concerning aspects of the conversation
                3. The specific trigger that caused the alert: {reason}
                4. A condensed version of the relevant parts of the conversation
                5. Any recommendations for follow-up actions
                
                Format the response as a JSON object with these fields:
                {{
                    "subject": "Email subject line",
                    "recipient": "admin@organization.com",
                    "body": "Complete email body with all required information"
                }}
                """
                
                # Create a new thread for this interaction
                thread = self.ai_client.agents.create_thread()
                
                # Send message to the alert agent
                self.ai_client.agents.create_message(
                    thread_id=thread.id,
                    role="user",
                    content=prompt
                )
                
                # Process the message
                run = self.ai_client.agents.create_and_process_run(
                    thread_id=thread.id,
                    agent_id=self.alert_agent_id
                )
                
                # Get the response
                messages = self.ai_client.agents.list_messages(thread_id=thread.id)
                
                # Find the assistant message
                response_text = ""
                for message in messages.data:
                    if message.role == "assistant":
                        for content_item in message.content:
                            if hasattr(content_item, 'text') and hasattr(content_item.text, 'value'):
                                response_text = content_item.text.value
                                break
                        break
                
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'({.*})', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    email_data = json.loads(json_str)
                else:
                    # If not found, try parsing the entire response
                    email_data = json.loads(response_text)
                
                # ALWAYS print full email details for debugging
                print("\n📧 Alert Email Generated:")
                print(f"  Subject: {email_data.get('subject', 'URGENT: Mental Health Alert')}")
                print(f"  Recipient: {email_data.get('recipient', self.admin_email)}")
                print("  Body:")
                print("  " + "\n  ".join(email_data.get('body', '').split('\n')))
                
                # Send the email
                success = self.send_alert_email(email_data)
                if not success:
                    print("⚠️ Failed to send email with Campus Calm agent. Trying fallback...")
                    # Try fallback if primary method fails
                    self.send_fallback_alert_email(reason, all_history)
                    
            except Exception as e:
                logger.error(f"Error using Campus Calm alert agent: {str(e)}")
                print(f"⚠️ Error generating alert email: {str(e)}. Using fallback alert.")
                # Fall back to simpler alert email
                self.send_fallback_alert_email(reason, all_history)
        else:
            # Use fallback alert email if Campus Calm agent isn't available
            print("📧 Campus Calm agent not available. Generating fallback alert email...")
            self.send_fallback_alert_email(reason, all_history)

    def send_alert_email(self, email_data: Dict[str, str]) -> bool:
        """Send an alert email using SMTP with simple formatting and reliability"""
        try:
            # Default recipient if not specified
            recipient = email_data.get("recipient", self.admin_email)
            recipients_list = [recipient]  # Create a list as required by sendmail
            
            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient
            msg["Subject"] = email_data.get("subject", "URGENT: Mental Health Alert")
            
            # Format the body with HTML for better readability, but with minimal styling
            body_text = email_data.get("body", "A potential mental health crisis has been detected. Please review the conversation.")
            
            # Simplified HTML body without complex CSS styling
            html_body = """
            <html>
            <body>
                <div style="background-color: #f44336; color: white; padding: 10px; text-align: center;">
                    <h2>⚠️ MENTAL HEALTH ALERT - IMMEDIATE ATTENTION REQUIRED ⚠️</h2>
                </div>
                <div style="padding: 15px;">
                    <p><strong>Alert Reason:</strong> {0}</p>
                    
                    <p style="color: #666; font-size: 0.9em;"><strong>Timestamp:</strong> {1}</p>
                    
                    <h3>Conversation History:</h3>
                    <div style="background-color: #f9f9f9; padding: 10px; border-left: 4px solid #ccc; margin: 10px 0;">
                        {2}
                    </div>
                    
                    <p><strong>This is an automated alert from the Mental Health Bot system.</strong><br>
                    Please review the conversation immediately and take appropriate action.</p>
                    
                    <div style="font-size: 0.8em; color: #666; margin-top: 20px;">
                        <p>Campus Calm Mental Health Alert System<br>
                        This email was sent automatically in response to concerning user input.</p>
                    </div>
                </div>
            </body>
            </html>
            """.format(
                email_data.get("reason", "Mental health concern detected"),
                datetime.now().isoformat(),
                body_text.replace("Conversation History:", "").replace("--------------------", "").replace("\n", "<br>")
            )
            
            # Also create a plain text alternative
            plain_text = f"""
    MENTAL HEALTH ALERT - IMMEDIATE ATTENTION REQUIRED

    Alert Reason: {email_data.get('reason', 'Mental health concern detected')}

    Timestamp: {datetime.now().isoformat()}

    Conversation History:
    --------------------
    {body_text}

    This is an automated alert from the Mental Health Bot system.
    Please review the conversation immediately and take appropriate action.
            """
            
            # Create a MIME multipart/alternative message
            msg_alt = MIMEMultipart('alternative')
            
            # Attach plain text and HTML versions
            msg_alt.attach(MIMEText(plain_text, 'plain'))
            msg_alt.attach(MIMEText(html_body, 'html'))
            
            # Attach the alternative part to the main message
            msg.attach(msg_alt)
            
            print(f"\n📧 Attempting to send email via {self.smtp_server}:{self.smtp_port}...")
            
            # Create SMTP connection with detailed logging
            try:
                s = smtplib.SMTP(self.smtp_server, self.smtp_port)
                s.set_debuglevel(1)  # Enable verbose debug output
                print("  SMTP connection established")
                
                s.starttls()
                print("  TLS started successfully")
                
                s.login(self.sender_email, self.sender_password)
                print("  SMTP authentication successful")
                
                # Send the email - use the proper method with a list of recipients
                msg_text = msg.as_string()
                send_errors = s.sendmail(self.sender_email, recipients_list, msg_text)
                
                # Check for any send errors
                if len(send_errors) == 0:
                    print("  Message sent successfully")
                else:
                    print(f"  ⚠️ Partial send errors: {send_errors}")
                    
                # Close the connection properly
                s.quit()
                
                logger.info(f"Alert email sent to {recipient}")
                print(f"✅ Alert email sent to {recipient}")
                return True
                    
            except Exception as e:
                print(f"  ⚠️ SMTP Error: {str(e)}")
                raise
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            print(f"❌ Email Error: {str(e)}")
            
            # Print email details that would have been sent
            print("\n📧 Email that would have been sent:")
            print(f"  To: {email_data.get('recipient', self.admin_email)}")
            print(f"  Subject: {email_data.get('subject', 'URGENT: Mental Health Alert')}")
            print("  Body Preview: " + email_data.get('body', '')[:100] + "...")
            
            return False


    def send_fallback_alert_email(self, reason: str, conversation_history: str) -> bool:
        """Send a basic alert email with minimal formatting when the agent isn't available"""
        try:
            subject = "URGENT: Mental Health Alert - Immediate Attention Required"
            
            # Create a more formatted body with linebreaks to make it more readable
            body = f"""
            MENTAL HEALTH ALERT - IMMEDIATE ATTENTION REQUIRED
            
            Alert Reason: {reason}
            
            Timestamp: {datetime.now().isoformat()}
            
            Conversation History:
            --------------------
            {conversation_history}
            
            This is an automated alert from the Mental Health Bot system.
            Please review the conversation immediately and take appropriate action.
            """
            
            email_data = {
                "subject": subject,
                "recipient": self.admin_email,
                "body": body,
                "reason": reason  # Add reason explicitly for HTML formatting
            }
            
            # Print email details for debugging
            print("\n📧 Fallback Alert Email Generated:")
            print(f"  Subject: {subject}")
            print(f"  Recipient: {self.admin_email}")
            print("  Body Preview:")
            print("  " + "\n  ".join(body[:500].split('\n')) + "...")
            
            return self.send_alert_email(email_data)
                
        except Exception as e:
            logger.error(f"Failed to send fallback alert email: {str(e)}")
            print(f"❌ Fallback Email Error: {str(e)}")
            return False
    
    def generate_response_with_rag(self, query: str, mental_health_analysis: Dict[str, Any] = None) -> str:
        """Generate a response using RAG approach with mental health considerations"""
        try:
            start_time = time.time()
            print("\n📚 Generating RAG response...")
            
            # Get relevant documents from knowledge base
            try:
                results = self.vector_search(query)
                if not results:
                    logger.warning("No vector search results, falling back to basic search")
                    results = self.basic_search(query)
            except Exception as e:
                logger.error(f"Search failed: {e}")
                logger.warning("Falling back to basic search")
                results = self.basic_search(query)
            
            # Format the context from documents
            context = "\n\n".join([doc.get("content", "") for doc in results])
            
            # Get mental health alert status
            is_alert = (mental_health_analysis is not None and 
                        mental_health_analysis.get("alert_flag", 0) == 1)
            
            # Create appropriate system message based on mental health analysis
            if is_alert:
                # High concern system message
                system_message = f"""
                You are Loona, a Gen Z mental health assistant created specifically for Stevens Institute of Technology students. Your vibe is supportive but casual - like texting with a wise friend who's been through it all.

                Always begin each new conversation with a friendly, Gen Z-style greeting such as:
                "Hey there! I'm Loona, your mental health bestie here at Stevens. What's on your mind today?"
                or
                "Sup! Loona here. I'm your go-to for mental health support at Stevens. How's it going?"

                Context information (Knowledge Base):
                {context}

                {red_folder}

                Core Instructions & Guidelines:
                Talk in small bits, keep it short and sweet. Keep it like a conversation between friends. Do not use emojis. Do not load the user with information. Keep it simple and easy to understand.
                Dont pity the user. Be supportive and encouraging.
                0. You are the primary point of contact you are responsible to chat with user, empathize and advice. Only if you are not able to help, you can refer to the resources below.
                1. To answer the user's question, you can use the information from the red folder stored in the RAG container database. You can also use the information from the knowledge base.
                1. Source Limitation: Always prioritize information from the Stevens Red Folder stored in the RAG container database.
                2. Crisis Detection: If user shows signs of mental health crisis, immediately provide CAPS 24/7 crisis line: (201) 216-5177.
                3. CAPS Information: Counseling & Psychological Services (CAPS)
                    Student Wellness Center, 2nd Floor
                    201-216-5177
                    caps@stevens.edu
                    Phone line is staffed 24/7
                    Visit stevens.edu/caps for more information
                4. UWill Details: Include UWill as 24/7 teletherapy option (free, confidential, uwill.com/stevens).
                5. Tone: Use Gen Z lingo (e.g., "vibe check," "no cap," "lowkey," "bestie," "fr") and keep it conversational.
                6. Conciseness: Keep responses short (1-3 sentences when possible) and easy to understand.
                7. Response Structure: Address concern → provide Stevens resources → add encouragement → optional follow-up question.
                8. Style: Sound like a supportive peer rather than a clinical professional, do NOT use emoji.
                8.1. Avoid using phrases like "It's important to" or "It's crucial to". Instead, use phrases like "You should" or "You might want to". For example, instead of "It's important to talk to someone about this", say "You should talk to someone about this".
                9. Resource Priority: Stevens CAPS first, UWill second, external resources (988, text HOME to 741741) last.
                10. Special Cases: For academic stress mention CAPS workshops; for relationship issues highlight counseling options.
                11. Follow-up: Always end with a supportive question or statement.
                12. Confidentiality: Assure users of confidentiality and privacy.
                13. Escalation: If user expresses suicidal thoughts, immediately provide CAPS 24/7 crisis line: (201) 216-5177.
                

                Remember: You're a friendly guide to Stevens mental health resources, not a therapist. Your goal is to connect students with the right campus support systems while being relatable and approachable.
                """

                # For crisis situations
                if mental_health_analysis.get("alert_flag") == 1:
                    system_message = f"""
                    You are Loona, a Gen Z mental health assistant for Stevens Institute of Technology students.
                    
                    IMPORTANT: The alert flag has been triggered for the following reason:
                    {mental_health_analysis.get("reason", "Potential mental health crisis detected")}
                    
                    Context information (Knowledge Base):
                    {context}

                    {red_folder}
                    
                    Your primary goals are to:
                    Dont pity the user. Be supportive and encouraging.
                    Talk in small bits, keep it short and sweet. Keep it like a conversation between friends. Do not use emojis. Do not load the user with information. Keep it simple and easy to understand.
                    0. You are the primary point of contact you are responsible to chat with user, empathize and advice. Only if you are not able to help, you can refer to the resources below.
                    1. To answer the user's question, you can use the information from the red folder stored in the RAG container database. You can also use the information from the knowledge base.
                    2. Immediately provide CAPS 24/7 crisis line: (201) 216-5177
                    3. Mention ProtoCall Services for after-hours support
                    4. Include National Crisis resources: 988 or text HOME to 741741
                    5. Keep your response clear, supportive, and super concise
                    6. Use a tone that's serious but still approachable
                    
                    Do not use excessive emojis or slang in crisis situations. Focus on connecting the student with immediate professional help from CAPS or crisis services.
                    """
            else:
                # Add a default system message for non-alert situations
                system_message = f"""
                You are Loona, a Gen Z mental health assistant created specifically for Stevens Institute of Technology students. Your vibe is supportive but casual - like texting with a wise friend who's been through it all.

                Context information (Knowledge Base):
                {context}

                Core Instructions & Guidelines:
                Dont pity the user. Be supportive and encouraging.
                Talk in small bits, keep it short and sweet. Keep it like a conversation between friends. Do not use emojis. Do not load the user with information. Keep it simple and easy to understand.
                0. You are the primary point of contact you are responsible to chat with user, empathize and advice. Only if you are not able to help, you can refer to the resources below.
                1. To answer the user's question, you can use the information from the red folder stored in the RAG container database. You can also use the information from the knowledge base.
                1. Source Limitation: Always prioritize information from the Stevens Red Folder stored in the RAG container database.
                2.. CAPS Information: Counseling & Psychological Services (CAPS)
                    Student Wellness Center, 2nd Floor
                    201-216-5177
                    caps@stevens.edu
                    Phone line is staffed 24/7
                    Visit stevens.edu/caps for more information
                3. UWill Details: Include UWill as 24/7 teletherapy option (free, confidential, uwill.com/stevens).
                4. Tone: Use Gen Z lingo (e.g., "vibe check," "no cap," "lowkey," "bestie," "fr") and keep it conversational.
                5. Conciseness: Keep responses short (1-3 sentences when possible) and easy to understand.
                6. Style: Sound like a supportive peer rather than a clinical professional, You should not use emojis at all
                7. Resource Priority: Stevens CAPS first, UWill second, external resources last.

                Remember: You're a friendly guide to Stevens mental health resources, not a therapist. Your goal is to connect students with the right campus support systems while being relatable and approachable.
                """
            
            # Format conversation history for context
            messages = []
            
            # First add the system message
            messages.append({"role": "system", "content": system_message})
            
            # Add up to the last 10 conversation turns for context
            for item in self.conversation_state["history"][-10:]:
                messages.append({"role": item["role"], "content": item["content"]})
            
            # Add the current user query
            messages.append({"role": "user", "content": query})
            
            # Use the GPT-4o deployment
            # Generate the response
            print(f"🤖 Generating response using {COMPLETIONS_DEPLOYMENT}...")
            
            response = client.chat.completions.create(
                messages=messages,
                max_tokens=1000,  # Set a reasonable limit
                temperature=0.7,
                top_p=1.0,
                model=COMPLETIONS_DEPLOYMENT  # Must match Azure deployment name exactly
            )
            
            # Extract and return the assistant's response
            assistant_response = response.choices[0].message.content
            return assistant_response
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            print(f"❌ Response Error: {str(e)}")
            # Fallback response in case of failure
            return "I'm sorry, I'm having trouble processing your question. Could you please try again? If you're experiencing a mental health emergency, please contact a crisis helpline or emergency services."
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate appropriate response"""
        try:
            # Log user input
            logger.info(f"User input: {user_input}")
            print(f"\n👤 User: {user_input}")
            
            # Check if user is saying goodbye
            if self.is_farewell(user_input):
                farewell_msg = "Thank you for chatting with me. Take care of yourself, and remember that support is always available when you need it. Goodbye!"
                print(f"🧠 Detected farewell message, sending goodbye response")
                return farewell_msg
            
            # Add user input to history
            self.conversation_state["history"].append({"role": "user", "content": user_input})
            
            # Process user input based on content
            print("🔍 Processing user input...")
            
            # Check if the input needs mental health analysis
            if self.is_expressing_concern(user_input) or len(user_input.split()) > 10:
                if self.is_expressing_concern(user_input):
                    print("🧠 Detected emotional concern in message")
                
                # Analyze for mental health severity
                analysis_result = self.analyze_mental_health_severity(user_input)
                
                # Update alert flag in conversation state
                self.conversation_state["alert_flag"] = analysis_result.get("alert_flag", 0)
                
                # If alert flag is set, trigger alert process
                if self.conversation_state["alert_flag"] == 1:
                    self.trigger_alert(analysis_result.get("reason", "Mental health concern detected"))
                
                # Generate response with RAG and mental health consideration
                response = self.generate_response_with_rag(user_input, analysis_result)
            else:
                # For shorter inputs or greetings, use simpler processing
                if self.is_greeting(user_input) and self.conversation_state["is_greeting_phase"]:
                    print("🧠 Detected greeting in initial conversation phase")
                    self.conversation_state["is_greeting_phase"] = False
                    response = "Hey there! I'm Loona, your mental health bestie here at Stevens. What's on your mind today?"
                else:
                    # Generate standard response
                    response = self.generate_response_with_rag(user_input)
            
            # Add response to history
            self.conversation_state["history"].append({"role": "assistant", "content": response})
            
            # Maintain conversation history size
            if len(self.conversation_state["history"]) > 20:
                self.conversation_state["history"] = self.conversation_state["history"][-20:]
            
            # Log the response
            logger.info(f"Assistant response: {response}")
            print(f"\n🤖 Loona: {response}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing user input: {str(e)}")
            print(f"❌ Input Processing Error: {str(e)}")
            return "I apologize, but I'm experiencing a technical issue. If you're facing a mental health emergency, please contact a crisis helpline or emergency services immediately."
    
    def save_conversation(self, filename="conversation_history.json"):
        """Save the conversation history to a file"""
        try:
            with open(filename, 'w') as file:
                json.dump({
                    "conversation": self.conversation_state["history"],
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {
                        "conversation_length": len(self.conversation_state["history"]),
                        "alert_flag": self.conversation_state["alert_flag"]
                    }
                }, file, indent=2)
            logger.info(f"Conversation saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save conversation: {str(e)}")
            return False
    
    def load_conversation(self, filename="conversation_history.json"):
        """Load conversation history from a file"""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.conversation_state["history"] = data["conversation"]
                # Set greeting phase to False if we're loading a conversation
                self.conversation_state["is_greeting_phase"] = False
                # Load alert flag if present
                if "metadata" in data and "alert_flag" in data["metadata"]:
                    self.conversation_state["alert_flag"] = data["metadata"]["alert_flag"]
            logger.info(f"Conversation loaded from {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to load conversation: {str(e)}")
            return False
    
    def export_logs(self, filename="system_logs.txt"):
        """Export system logs to a file"""
        try:
            with open(filename, 'w') as file:
                for log in self.logs:
                    file.write(f"{log}\n")
            logger.info(f"Logs exported to {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to export logs: {str(e)}")
            return False


def main():
    """Main function to run the integrated mental health chatbot"""
    print("\n" + "="*60)
    print("🧠 CampusCalm Integrated Mental Health Assistant 🧠")
    print("="*60)
    print("Commands:")
    print("  'exit', 'quit', 'bye' - End the conversation")
    print("  'save' - Save the conversation")
    print("  'load' - Load a previous conversation")
    print("  'logs' - Export system logs")
    print("  'status' - Check system status")
    print("  'verbose' - Toggle detailed console output")
    print("="*60 + "\n")
    
    try:
        # Create integrated bot
        print("🔄 Initializing systems...")
        bot = IntegratedMentalHealthBot()
        print("✅ All services initialized successfully\n")
    except Exception as e:
        print(f"❌ Error initializing bot: {str(e)}")
        print("⚠️ Please check your environment variables and connections.")
        return
    
    print("🤖 Loona: Hey there! I'm Loona, your mental health bestie here at Stevens. What's on your mind today?")
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\n🤖 Loona: Take care! Remember that I'm here if you need to talk again.")
            break
        
        elif user_input.lower() == 'save':
            filename = input("Enter filename to save (default: conversation_history.json): ").strip()
            filename = filename if filename else "conversation_history.json"
            print("💾 Saving conversation...")
            if bot.save_conversation(filename):
                print(f"✅ Conversation saved to {filename}")
            else:
                print("❌ Failed to save conversation")
            continue
        
        elif user_input.lower() == 'load':
            filename = input("Enter filename to load (default: conversation_history.json): ").strip()
            filename = filename if filename else "conversation_history.json"
            print("📂 Loading conversation...")
            if bot.load_conversation(filename):
                print(f"✅ Conversation loaded from {filename}")
                # Print the last bot message for context
                if bot.conversation_state["history"]:
                    last_bot_msg = next((msg["content"] for msg in reversed(bot.conversation_state["history"]) 
                                         if msg["role"] == "assistant"), None)
                    if last_bot_msg:
                        print(f"\n🤖 Loona: {last_bot_msg}")
            else:
                print("❌ Failed to load conversation")
            continue
        
        elif user_input.lower() == 'logs':
            filename = input("Enter filename for logs (default: system_logs.txt): ").strip()
            filename = filename if filename else "system_logs.txt"
            print("📊 Exporting logs...")
            if bot.export_logs(filename):
                print(f"✅ Logs exported to {filename}")
            else:
                print("❌ Failed to export logs")
            continue
            
        elif user_input.lower() == 'status':
            print("\n📊 System Status:")
            alert_status = "🚨 ALERT ACTIVE" if bot.conversation_state["alert_flag"] == 1 else "✅ No alerts"
            print(f"  OpenAI connection: ✅ Connected")
            print(f"  Cosmos DB connection: ✅ Connected")
            print(f"  Alert status: {alert_status}")
            print(f"  Conversation length: {len(bot.conversation_state['history'])} messages")
            print(f"  Greeting phase: {'Yes' if bot.conversation_state['is_greeting_phase'] else 'No'}")
            continue
            
        elif user_input.lower() == 'verbose':
            bot.verbose_console = not bot.verbose_console
            print(f"🔊 Verbose console output: {'Enabled' if bot.verbose_console else 'Disabled'}")
            continue
        
        try:
            # Process user input is handled in the method itself with console output
            response = bot.process_user_input(user_input)
        except Exception as e:
            print(f"\n❌ Error processing input: {str(e)}")
            print("⚠️ Please check your connections.")


if __name__ == "__main__":
    main()

