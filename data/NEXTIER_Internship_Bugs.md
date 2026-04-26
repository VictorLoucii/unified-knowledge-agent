NEXTIER TECHNOLOGIES

MY ROLE: REACT NATIVE INTERN

## Project Workflow & Safety Rules

• **Use Yarn Only**: Avoid \`npm\` commands entirely to prevent
\`package-lock.json\` conflicts. Use \`yarn install\`, \`yarn start\`,
etc.

• **Selective Git Staging**: Instead of \`git add .\`, use \`git add
src/\` to ensure only your code changes are tracked and
environment-specific files (like \`local.properties\`) stay local.

• **Build Strategy**: If the app is running in the emulator, skip
\`./gradlew clean\` before building to preserve working native links.
Use \`./gradlew assembleRelease\` directly.

• **APK Location**: Found in
\`android/app/build/outputs/apk/release/app-release.apk\`.

Note: i created a classic token and entered it as a password

Last login: Sun Feb 22 17:36:48 on ttys000

victorloucii@victors-MacBook-Air \~ % cd Nexteir_Technologies

victorloucii@victors-MacBook-Air Nexteir_Technologies % git clone
https://github.com/Rootree-AIO/CHHIRO_COMMUNITY_MOBILE_APP.git

Cloning into \'CHHIRO_COMMUNITY_MOBILE_APP\'\...

remote: Repository not found.

fatal: repository
\'https://github.com/Rootree-AIO/CHHIRO_COMMUNITY_MOBILE_APP.git/\' not
found

victorloucii@victors-MacBook-Air Nexteir_Technologies % git clone
https://VictorNeisa@github.com/Rootree-AIO/CHHIRO_COMMUNITY_MOBILE_APP.git

Cloning into \'CHHIRO_COMMUNITY_MOBILE_APP\'\...

Password for \'https://VictorNeisa@github.com\':

remote: Enumerating objects: 3922, done.

remote: Counting objects: 100% (1618/1618), done.

remote: Compressing objects: 100% (1140/1140), done.

remote: Total 3922 (delta 1071), reused 938 (delta 472), pack-reused
2304 (from 1)

Receiving objects: 100% (3922/3922), 5.64 MiB \| 3.30 MiB/s, done.

Resolving deltas: 100% (2563/2563), done.

victorloucii@victors-MacBook-Air Nexteir_Technologies % cd
CHHIRO_COMMUNITY_MOBILE_APP

victorloucii@victors-MacBook-Air CHHIRO_COMMUNITY_MOBILE_APP % git
checkout bug/hot-fixes-enhancement

branch \'bug/hot-fixes-enhancement\' set up to track
\'origin/bug/hot-fixes-enhancement\'.

Switched to a new branch \'bug/hot-fixes-enhancement\'

victorloucii@victors-MacBook-Air CHHIRO_COMMUNITY_MOBILE_APP % git
checkout -b Victor/fix-enhancements

Switched to a new branch \'Victor/fix-enhancements\'

victorloucii@victors-MacBook-Air CHHIRO_COMMUNITY_MOBILE_APP % git
branch

\* Victor/fix-enhancements

bug/hot-fixes-enhancement

main

Here is the breakdown of what happened in your terminal and why those
steps are the foundation of professional coding.

### **Part 1: Terminal Command Breakdown**

  -----------------------------------------------------------------------
  **Command**              **What it actually  **The \"Why\"**
                           did**               
  ------------------------ ------------------- --------------------------
  **cd                     Moved your terminal You need to be in the
  Nexteir_Technologies**   \"focus\" into that right physical location on
                           folder.             your hard drive before
                                               downloading code.

  **git clone \...**       Downloaded a full   This creates a local
                           copy of the project \"mirror\" of the project
                           from GitHub\'s      so you can work offline.
                           servers to your     
                           Mac.                

  **Password for\...**     This was the        Since the project is
                           security gate where private, GitHub needed to
                           you pasted your     verify you are VictorNeisa
                           **Classic Token**.  and have permission.

  **git checkout           Switched your files Teams work on different
  \[branch\]**             from the default    \"versions\" of code
                           version to the      simultaneously. This
                           specific \"bug      ensured you are looking at
                           fix\" version.      the right one.

  **git checkout -b        Created a **brand   **Crucial:** This ensures
  \[name\]**               new sandbox** for   that if you make a
                           just your changes.  mistake, you don\'t break
                                               the team\'s main code. You
                                               are working in a safe
                                               \"draft\" space.

  **git branch**           Listed all local    This is your \"GPS\" to
                           branches and put a  confirm you are exactly
                           \* next to the      where you think you are.
                           active one.         
  -----------------------------------------------------------------------

### **Your Next Step**

**Since you have your branch ready and VS Code open, you are in the
\"active development\" phase. Think of your branch as a private draft of
a document that nobody else can see until you \"publish\" it.**

**Here is the exact professional workflow to follow from this moment
until your code is live on GitHub.**

### **Phase 1: Making Changes**

1.  **Code: Edit your files in VS Code.**

2.  **Save: Save your files (Cmd+S) just like any other document.**

3.  **Check Status: Periodically go back to your terminal and type:**

4.  **Bash**

**git status**

5.  

6.  ***You will see the names of the files you changed highlighted in
    red.***

### **Phase 2: The \"Big Three\" (Saving to GitHub)**

**When you reach a point where you are happy with your work, run these
three commands in order:**

#### **1. Stage the changes**

**This tells Git, \"I want to include these specific changes in my next
save.\"**

**Bash**

**git add .**

***(The dot means \"add everything I changed\").***

#### **2. Commit the changes**

**This creates a permanent snapshot of your work with a label.**

**Bash**

**git commit -m \"Brief description of what I fixed\"**

***Tip: Keep your messages clear, like \"Fixed login button alignment\"
or \"Updated app theme colors\".***

#### **3. Push to GitHub**

**This sends your local branch and all its commits up to the GitHub
server.**

**Bash**

**git push origin Victor/fix-enhancements**

***Note: Since you are using a new branch, GitHub might give you a long
command to copy and paste for the first push---just copy/paste whatever
it suggests!***

### **Phase 3: Merging (The Final Goal)**

**After you push, your code is on GitHub, but it is still only in your
Victor/fix-enhancements branch. To get it into the team\'s main
project:**

1.  **Go to the GitHub website.**

2.  **You will see a yellow bar at the top that says \"Compare & pull
    request\". Click it.**

3.  **Add a description of what you did and click Create Pull Request.**

4.  **Your team lead will review your code and \"Merge\" it into the
    main project.**

### **Summary Checklist**

- **Work: Edit and Save in VS Code.**

- **Stage: git add .**

- **Save Snapshot: git commit -m \"message\"**

- **Upload: git push origin your-branch-name**

### **Pro Tip:**

**If you want to see exactly what lines you changed before adding them,
type git diff. It will show you the \"old\" code in red and your \"new\"
code in green.**

**Would you like me to show you how to handle a situation where a
teammate changes the main code while you are still working on your
branch?**

NEXT STEPS:

The logs show that your npm install was successful and, more
importantly, your pod install (the hardest part on a Mac) finished
completely with **\"Pod installation complete!\"** All the
\"deprecated\" warnings you saw in yellow at the beginning are normal;
they are just older packages the team is using, and you can ignore them.

### **Why you still see red errors in VS Code:**

Even though you installed everything correctly, VS Code is likely still
\"remembering\" the errors from before you ran the install. It hasn\'t
refreshed its internal map of the project.

**Do these two things to clear the errors:**

1.  **Restart the TS Server:**

    - In VS Code, press Command + Shift + P.

    - Type **\"Restart TS Server\"** and hit Enter.

2.  **Reload Window:**

    - Press Command + Shift + P again.

    - Type **\"Reload Window\"** and hit Enter.

### **Now, let\'s run the app on Android!**

Since you mentioned you have **Android Studio** and want to run it
there, follow these steps exactly:

**Step 1: Open the Emulator**

- Open **Android Studio**.

- Go to **Device Manager** (top right icon).

- Click the **Play (Triangle)** button next to your virtual phone to
  start the emulator.

**Step 2: Start the \"Metro\" Bundler**

- In your terminal, inside the CHHIRO_COMMUNITY_MOBILE_APP folder, run:

- Bash

npx react-native start

- 

- 

- *Keep this terminal window open!* It needs to run the whole time you
  are coding.

**Step 3: Launch the app on the phone**

- Open a **NEW** terminal tab (Command + T) and run:

- Bash

npx react-native run-android

- 
- 

### **What to look for:**

- The first time you run this, it will take **5-10 minutes** to build.

- You will see a green bar in the \"Metro\" terminal when it starts
  \"Loading from 10.0.2.2\".

- If the app appears on your emulator screen, **you are officially an
  active developer on the project.**

# Problem 1

When you are dropped into a massive React Native codebase and have
\*\*absolutely no clue\*\* where a specific screen or button is located,
here is the standard, step-by-step approach professional developers use
to hunt down the exact file:

\### 1. The \"Static Text\" Search (Fastest Method)

If there is any hardcoded text on the screen, this is the quickest way
to find the file.

\* \*\*Look at the screen:\*\* For example, in your first screenshot,
the screen says \`\"0 Connections \| 0 Followers\"\` or \`\"Founder at
Mercedes AMG\"\`.

\* \*\*Global Search:\*\* Open your code editor (VS Code/Android
Studio), press \*\*\`Cmd + Shift + F\`\*\* (Mac) or \*\*\`Ctrl + Shift +
F\`\*\* (Windows), and search for exactly that text: \`\"0
Connections\"\` or \`\"Experience\"\`.

\* \*\*Result:\*\* This will usually take you directly to the file
rendering that screen.

**\### 2. The Element Inspector (Most Reliable)**

This is exactly what you just did, and it is the best method when the
text is dynamic (user-generated) or missing (like your empty button).

\* Press \*\*\`Cmd + M\`\*\* (or \`Ctrl + M\`) on the emulator.

\* Click \*\*\"Toggle Element Inspector\"\*\*.

\* Tap the mystery element.

\* Look at the \*\*Component Breadcrumbs\*\* at the top (e.g.,
\`ProfileTopTabs \> AboutTab \> EditAbout\`).

\* \*\*Global Search:\*\* Now, do a global search (\`Cmd/Ctrl + Shift +
F\`) for the most unique component name in that list, like \`function
EditAbout\` or \`const EditAbout\`.

\### 3. The \"Unique Styling\" Search (The Hacker Method)

If a component has a very specific color, icon, or unique styling, use
that to your advantage.

\* Open the Element Inspector and tap the element.

\* Look at the styling panel (like in your last screenshot).

\* Notice the exact color? \*\*\`#FA6400\`\*\*.

\* \*\*Global Search:\*\* Search your entire project for \`#FA6400\` or
\`FA6400\`. Since that specific orange isn\'t used everywhere, the
search results will be very small, leading you straight to the correct
\`StyleSheet\` and file.

\### 4. React DevTools (The Advanced Method)

If the built-in inspector isn\'t giving you enough clues, you can use
React\'s official debugging tool.

\* Open your terminal and run: \`npx react-devtools\`

\* Open your in-app Dev Menu (\`Cmd + M\`) and click \*\*\"Open
DevTools\"\*\*.

\* This opens a window on your computer that looks exactly like
Chrome\'s \"Inspect Element\", but for React Native.

\* You can click through the entire component tree, and on the
right-hand panel, it will explicitly tell you the \*\*source file name
and line number\*\* for whatever component you click on.

\### Summary Checklist for a \"No Clue\" Situation:

1\. Try searching for \*\*static text\*\* on the screen.

2\. If no text, use the \*\*Element Inspector\*\* to find the
\`\<ComponentName\>\`. Search for that name.

3\. If no clear component name, use the Inspector to find a \*\*unique
color hex code\*\* and search for that.

# Problem 2

![](data/media_dump/media/image5.png){width="2.15625in"
height="4.302638888888889in"}![](data/media_dump/media/image1.png){width="1.9322922134733158in"
height="4.286578083989501in"}

**filepath : src/screens/profile/components/EditAbout.tsx**

**Profile Editing - \"About\" Section CTA Issue:**

The Call to Action (CTA) label for saving edits in the \"About\" section
of the profile is missing. The label appears to disappear shortly after
the user begins editing or entering new information.

Here is a complete, detailed summary of the issue, the debugging
process, and the final solution we implemented for your React Native
app:

\### 1. The Initial Problem

**In the Profile Editing screen, specifically within the \"About\"
section modal, the Call to Action (CTA) button at the bottom of the
screen (the orange button meant to save/submit changes) was completely
blank. The label text would mysteriously disappear, especially when the
user tapped the text input to begin typing.**

\### 2. Locating the Source File

Because the codebase was large, we needed to find the exact file
rendering that empty button.

\* You opened the \*\*React Native Dev Menu\*\* (\`Cmd/Ctrl + M\`) in
the Android emulator.

\* You activated the \*\*Element Inspector\*\* and tapped directly on
the empty orange button.

\* The Inspector revealed the component tree breadcrumbs: \`\... \>
AboutTab \> EditAbout \> Button \> TouchableOpacity\`.

\* This pinpointed that the bug was located inside a custom component
named \*\*\`EditAbout.tsx\`\*\*.

\### 3. Analyzing the Code & First Attempt

Once you provided the code for \`EditAbout.tsx\`, we noticed a missing
prop. The custom \`\<Button\>\` component for \"Submit\" was missing its
\`textStyle={styles.sendButtonText}\` prop, meaning it wasn\'t receiving
its designated white text color (\`theme.colors.card\`).

However, adding this style \*did not\* fix the issue. The text was still
disappearing when typing began.

\### 4. Discovering the Root Cause: Layout & Padding Collision

We looked back at the Element Inspector metrics you provided and found
the actual culprit. It was a mathematical layout collision causing React
Native\'s engine to hide the text:

**\* \*\*The Component Height:\*\* The button was being forced to a
total height of \*\*\`32px\`\*\* (likely caused by the
\`size=\"small\"\` prop on the custom Button component).**

**\* \*\*The Padding:\*\* The stylesheet was applying \`paddingVertical:
theme.spacing.md\` (which translated to \`16px\` of padding on the top,
and \`16px\` on the bottom).**

**\* \*\*The Math:\*\* \`16px (top) + 16px (bottom) = 32px\`.**

**\* \*\*The Result:\*\* The padding consumed 100% of the button\'s
height, leaving \*\*\`0 pixels\`\*\* of vertical space for the
\`\<Text\>\` element to render.**

\*\*Why it vanished specifically when typing:\*\* When you tapped the
input, the keyboard opened. The \`KeyboardAvoidingView\` recalculates
the screen layout, slightly squishing the flex containers. This tiny
squish triggered the 0-pixel collision, forcing React Native to clip
(hide) the text completely to prevent it from bleeding out of its
container.

\### 5. The Final Fix

To solve this, we gave the text room to breathe by removing the
artificial constraints squeezing the button.

\*\*1. Updated the JSX (Component Props):\*\* file: **EditAbout.tsx**

We removed the \`size=\"small\"\` prop from both buttons to let them
size naturally, and we ensured the \`textStyle\` prop was properly
passed.

\`\`\`tsx

\<View style={styles.actionSection}\>

\<Button

style={styles.cancelButton}

textStyle={styles.cancelButtonText}

title={t(\'profile.editSkills.cancel\')}

// size=\"small\" \<\-- REMOVED

onPress={handleClose}

/\>

\<Button

style={styles.sendButton}

textStyle={styles.sendButtonText} // \<\-- ADDED MISSING STYLE PROP

title={t(\'profile.editAbout.submit\')}

// size=\"small\" \<\-- REMOVED

variant=\"primary\"

onPress={handleSubmit}

/\>

\</View\>

\`\`\`

\*\*2. Updated the Stylesheet:\*\*

We removed the conflicting vertical padding from the buttons and added a
rule to prevent the keyboard from squishing the container.

\`\`\`tsx

actionSection: {

flexDirection: \'row\',

paddingHorizontal: theme.spacing.md,

paddingVertical: theme.spacing.md,

paddingBottom: theme.spacing.lg,

gap: theme.spacing.md,

backgroundColor: theme.colors.background,

flexShrink: 0, // \<\-- ADDED: Prevents keyboard from squishing the row

},

cancelButton: {

flex: 1,

// paddingVertical: theme.spacing.md, \<\-- REMOVED: Conflicting padding

borderRadius: theme.borderRadius.md,

alignItems: \'center\',

justifyContent: \'center\',

backgroundColor: \'transparent\',

},

sendButton: {

flex: 2,

backgroundColor: theme.colors.primary,

// paddingVertical: theme.spacing.md, \<\-- REMOVED: Conflicting padding

borderRadius: theme.borderRadius.md,

alignItems: \'center\',

justifyContent: \'center\',

},

\`\`\`

\### 6. The Result

By applying these changes, the button was able to calculate its height
accurately based on the text inside it, rather than being forced into a
32px box filled entirely with padding. The \"Submit\" text now renders
perfectly in white against the orange background, regardless of whether
the user is actively typing or the keyboard is open!

# Problem 3

When navigating to the **Active Investment** or **Investment Portfolio**
tabs, the alignment of the investment details and the **Add Investment**
button appears inconsistent. Additionally, the design of the **Add
Investment** button is not uniform with other buttons used across the
application, and this should be standardized to maintain design
consistency. (Victor)\
\
![](data/media_dump/media/image4.png){width="1.796875546806649in"
height="3.979745188101487in"}![](data/media_dump/media/image3.png){width="1.7864588801399826in"
height="3.9771522309711287in"}

The first image was the problem and the second one is the solution
output.

**filepath :
src/screens/investor/investment-portfolio/components/InvestmentsList.tsx**

Answer:

So the original code had mode = "outline" i changed it to mode =
"contained" to match the device theme button line in Recommend
Communities 'Join' button.

Steps i did:

To summarize, you fixed the visibility and layout issues of your \"Add\"
button by moving away from generic style props and using the specific
internal props provided by react-native-paper.

Here is the detailed breakdown of the fix based on your implementation
and the documentation:

### **1. Fixing Text & Icon Color**

**The Problem:** In mode=\"contained\", the standard style prop or color
prop often targets the background of the button rather than the content.

**The Fix:** You used **labelStyle**.

- This prop specifically targets the text and the icon inside the
  button.

- By setting labelStyle={{ color: !theme.isDark ? \'black\' : \'white\'
  }}, you ensured that the button content remains readable regardless of
  whether the app is in Light or Dark mode.

### **2. Adjusting Icon-to-Text Spacing**

**The Problem:** The + icon and the \"Add\" text were spaced further
apart than desired by default.

**The Fix:** You applied **marginLeft** inside the labelStyle.

- Because react-native-paper treats the icon and text as part of the
  same label container, applying a margin here allowed you to \"pull\"
  the text closer to the icon.

- **Best Practice:** Instead of using a hardcoded number like 2, you can
  use theme.spacing.xs to keep the design consistent with the rest of
  your app\'s layout.

### **3. Controlling Internal Padding**

**The Problem:** Standard padding in the style prop often affects the
outer container, not the touchable area or the internal alignment.

**The Fix:** Use **contentStyle**.

- This prop styles the View that wraps both the icon and the label.

- To \"play around\" with the button\'s internal feel, you can adjust
  paddingHorizontal or height here.

### **Final Corrected Structure:**

JavaScript

\<Button

mode=\"contained\"

icon={\'plus\'}

compact

onPress={() =\> setShowAddInvestmentModal(true)}

// Styles the outer button wrapper

style={{ marginBottom: theme.spacing.md }}

// Styles the inner container (padding/height)

contentStyle={{ paddingHorizontal: theme.spacing.sm }}

// Styles the actual text and icon (color/spacing)

labelStyle={{

color: !theme.isDark ? \'black\' : \'white\',

marginLeft: theme.spacing.xs

}}

\>

Add

\</Button\>

### **Why this works according to the Doc:**

The Stack Overflow document you uploaded confirms that in \"contained\"
mode, the color property is interpreted as the **background color**. To
change the foreground (text/icon), you must target the label
specifically or wrap the content in a custom Text component. Using
labelStyle is the cleanest, built-in way to achieve this without nesting
extra components.

# Problem 4

On the **Answer** screen for a question, the alignment of the **Add
Media** buttons and the spacing between them appear inconsistent
compared to similar sections elsewhere in the application. Additionally,
the **Answer** button is not properly aligned.

Kindly review and adjust the spacing and alignment to ensure consistency
with the rest of the application's design standards. (Victor)

**Filepath:
src/screens/community/components/common/AnswerDialogCard.tsx**

I just added styles similar to EditAbout.tsx file to keep consistency
for cta buttons.

![](data/media_dump/media/image6.png){width="2.3802088801399823in"
height="5.300029527559055in"}![](data/media_dump/media/image7.png){width="2.3867115048118985in"
height="5.307292213473316in"}

Answer:

## **1. How you found the source code**

Finding the location was the hardest part because of the deep nesting.
Here was the logical trail:

- **Step 1: The Inspector.** You used the React Native Inspector and
  Chrome DevTools to see the component hierarchy. It told you the
  component was named CommunityCard, but you discovered there were
  multiple files with that same name.

- **Step 2: Component Props.** You logged the props using \$r in the
  console. This showed that the component was receiving community data,
  which helped narrow down which \"Community Card\" was active.

- **Step 3: The Breadcrumb Trail.** You looked at
  CommunityDashboard.tsx, saw it imported CommunityTopTabs, which led
  you to QuestionU.tsx.

- **Step 4: Dependency Discovery.** Inside QuestionU.tsx, you saw that
  the \"Answer\" button wasn\'t just code in that file; it was a
  sub-component called AnswerDialogCard.

- **Step 5: The Final Destination.** You followed the import to
  src/screens/community/components/common/AnswerDialogCard.tsx, which
  contained the actual UI for the button and the media toolbar.

## **2. Summary of the UI Fixes**

To address the feedback regarding inconsistent spacing and alignment,
you made the following changes:

### **The \"Answer\" Button (CTA)**

- **Reduced Size:** You changed the container height from **35 to 28**.

- **Refined Icon:** You shrunk the IconButton size from **22 to 18** and
  set the marginLeft to **-6** to balance the visual weight.

- **Typography:** You adjusted the fontSize to theme.fonts.sizes.sm to
  make the text \"Answer\" proportional to the smaller button.

- **Consistency:** Added a borderWidth: 0.8 and borderRadius: r12 to
  ensure the button looked crisp and matched the app\'s standard button
  styles.

### **The Media Toolbar (Alignment)**

- **Consistent Gapping:** In the AttachmentToolbar, you used a
  flexDirection: \'row\' with a **negative gap (gap: -8)** and removed
  the default IconButton margins.

- **Visual Logic:** This grouped the camera, image, and paperclip icons
  together tightly, solving the \"inconsistent spacing\" issue Victor
  reported.

- **Standardization:** By stripping the default library margins and
  applying your own, you ensured the icons align perfectly on a single
  horizontal axis.

### **Why this is a solid fix:**

By making these items smaller and more tightly grouped, you\'ve improved
the **Information Density**. The screen now looks less \"cluttered,\"
and the \"Answer\" action is clearly defined without taking up too much
vertical space in the feed.

**Now that you\'ve fixed the UI, would you like me to help you verify if
there are any other screens using AnswerDialogCard that might have been
affected by these changes?**

# Problem 5

## **The Problem: Unrestricted File Uploads**

Previously, the \"Add Education\" form allowed users to upload a variety
of file formats, specifically both **images** and **PDFs**.

This led to several issues:

- **Inconsistent Data:** Users could upload photos or screenshots
  instead of official documents.

- **UX Confusion:** The UI suggested \"images and docs,\" which didn\'t
  guide the user toward providing formal academic proof.

- **Security/Validation Gaps:** There was no logic at the code level to
  stop a user from selecting a file type that the system might not
  actually want for educational records.

## **The Original Code**

In the original version of EducationForm.tsx, the validation and the
input configuration were broad and inclusive of image types.

### **1. The Schema (No Type Checking)**

TypeScript

// Original Zod Schema

media: z.array(z.any()).optional(),

### **2. The Form Field Configuration (Allowed Images)**

TypeScript

// Original createFormFields config

{

type: \'document\',

control,

name: \'media\',

label: \'Media\',

placeholder: \'Add media (images, docs, etc.)\',

error: errors.media,

allowedTypes: \[\'image/\*\', \'application/pdf\'\], // Allowed
everything

multiple: true,

maxFiles: 5,

maxFileSizeMB: 10,

documentType: DocumentType.DOCUMENT,

},

## **The Solution (Your Changes)**

You updated the code to enforce a strict PDF-only policy. This was
achieved by tightening the validation schema and restricting the native
file picker.

### **1. The Updated Schema (The \"Double Check\")**

You added a refinement to ensure that even if the picker fails, the form
logic will reject anything that isn\'t a PDF.

TypeScript

media: z.array(z.any()).optional().refine(

(files) =\> !files \|\| files.every(file =\> file.type ===
\'application/pdf\' \|\| file.mimeType === \'application/pdf\'),

{ message: \"Only PDF files are allowed\" }

),

### **2. The Updated Form Field (The \"UI Filter\")**

You modified the configuration to limit what the user sees when their
phone\'s file gallery opens and updated the instructional text.

TypeScript

{

type: \'document\',

control,

name: \'media\',

label: \'Media\',

placeholder: \'Add PDF documents\', // Updated text

error: errors.media,

allowedTypes: \[\'application/pdf\'\], // Restricted picker to PDF only

multiple: true,

maxFiles: 5,

maxFileSizeMB: 10,

documentType: DocumentType.DOCUMENT,

},

By doing this, you\'ve ensured that the data collected is professional
and consistent.

Since you\'ve restricted the input to PDFs, would you like me to help
you clean up the **EducationTab.tsx** file so it doesn\'t try to render
image previews anymore?

# Problem 6

You were debugging something very real --- and the confusion came from
**multiple layers interacting at once**:

- React Hook Form

- Zod validation

- Modal visibility state

- Parent → child contract

- API mutation state

When forms stop responding with "nothing happens", it's almost never
random. It's almost always one of these layers blocking execution.

# **🔎 What Was Actually Happening (Root Cause Analysis)**

## **1️⃣ The Button Click Was Being Blocked**

When you clicked **Update Details**, you saw:

- Autocomplete logs

- But **no "UPDATE BUTTON CLICKED" log**

- No validation success

- No validation failure

That means:

👉 The onPress was never executing.

There are only 3 real reasons that happens in React Native:

1.  The button is disabled

2.  The component is not mounted

3.  The touch event is being swallowed by something

In your case, the main culprit was this:

loading={mutating}

disabled={mutating}

If mutating is stuck true, the button is completely dead.\
A disabled button **does not fire onPress at all**.

So from the outside it looks like:

> "React Hook Form is broken."

But actually:

> "The button never fired."

## **2️⃣ Zod + null vs undefined (Silent Validator Blocking)**

Your backend sometimes sends:

gender: null

avatarUrl: null

But your schema originally used:

z.string().optional()

Here's the important rule:

  ------------------------------------------
  **Zod Type**  **Accepts        **Accepts
                undefined**      null**
  ------------- ---------------- -----------
  .optional()   ✅               ❌

  .nullable()   ❌               ✅

  .nullish()    ✅               ✅
  ------------------------------------------

If Zod receives null but expects optional, it fails validation.

React Hook Form then refuses submission.

If you don't log errors manually, it looks like:

> "The button does nothing."

But it's actually:

> "Validation failed silently."

That's why .nullish() was the correct fix.

## **3️⃣ Parent--Child Contract Mismatch**

This was the second major bug.

Child (BasicProfileEdit) was sending:

{

locationId

}

Parent (Profile.tsx) was expecting:

data.location.value

That property no longer existed.

So when parent executed:

location: data.location.value

It crashed internally before calling the mutation.

Result:

- No API call

- No modal close

- No visible error

This is called a **payload contract mismatch**.

This is one of the most common bugs in real-world apps.

# **🧠 Why This Felt So Confusing**

Because multiple things were happening:

- Validation could block submission

- Disabled button could block submission

- Parent could crash silently

- Mutation state could lock UI

- Modal only closes on success

Each layer can independently stop the flow.

That's why debugging forms requires structured thinking.

# **✅ Final Stable Implementation (Correct Setup)**

Here's the clean architecture you should keep for future reference.

## **✔ 1. Zod Schema (Bulletproof Against Backend Nulls)**

const profileSchema = z.object({

displayName: z.string().min(1, \'Display name is required\'),

titleLine: z.string().min(1, \'Title line is required\'),

avatarUrl: z.string().nullish(),

location: z.object({

label: z.union(\[z.string(), z.number()\]).nullish(),

value: z.union(\[z.string(), z.number()\]).nullish(),

})

.nullish()

.refine(data =\> !!data?.value, {

message: \'Location is required\'

}),

gender: z.object({

label: z.union(\[z.string(), z.number()\]).nullish(),

value: z.union(\[z.string(), z.number()\]).nullish(),

}).nullish(),

});

This prevents:

- Backend null crashes

- Silent validation failure

## **✔ 2. Button Debug Pattern (Permanent Safe Pattern)**

For debugging forms, always use this pattern:

onPress={() =\> {

console.log(\"🚨 BUTTON CLICKED\");

handleSubmit(

(data) =\> {

console.log(\"✅ VALIDATION SUCCESS:\", data);

handleFormSubmit(data);

},

(errors) =\> {

console.log(\"❌ VALIDATION FAILED:\", errors);

}

)();

}}

This guarantees:

- You know if click fired

- You know if validation failed

- You know if validation passed

Never debug blindly.

## **✔ 3. Parent Submit Function (Correct Contract)**

Parent must match exactly what child sends:

const handleSubmitProfileEdit = (data: {

displayName: string;

titleLine: string;

avatarUrl?: string;

locationId?: number;

genderId?: number;

genderName?: string;

}) =\> {

const payload = {

fullName: data.displayName,

avatarUrl: data.avatarUrl,

locationId: data.locationId,

title: data.titleLine,

genderId: data.genderId,

genderName: data.genderName,

};

updateUserProfile(payload, {

onSuccess: () =\> {

refetch();

handleCloseEditModal();

},

});

};

Child sends → Parent expects → API receives\
No guessing.

# **🧠 The Big Lesson (Very Important)**

When "nothing happens" in a form:

### **Always check in this order:**

1.  Is the button disabled?

2.  Does onPress fire?

3.  Did validation fail?

4.  Did parent receive payload?

5.  Did API fire?

6.  Did success callback execute?

Forms fail in layers.\
Debug layer by layer.

# Problem 7

## **✅ What Brought the Underline in Profile-\>about/eduction... tabs**

The key change is this block: in src/screens/profile/ProfileTopTabs.tsx

To add and shorten the underline (indicator) from both the left and
right sides, you just need to swap \*\*padding\*\* for \*\*margin\*\* in
your tab item styles.

Right now, the underline matches the full width of your tab. Because you
are using \`paddingHorizontal\`, the tab itself is stretched wider than
the text.

Make these two quick changes in your \`screenOptions\`:

\*\*1. Update \`tabBarItemStyle\`\*\*

Remove \`paddingHorizontal\` and replace it with \`marginHorizontal\`.
Margin keeps the spacing between tabs but shrinks the tab\'s actual
width strictly to the text size.

\`\`\`javascript

tabBarItemStyle: {

width: \'auto\',

marginHorizontal: 15, // \<\-- Add this

// paddingHorizontal: 20, \<\-- Remove this

},

\`\`\`

\*\*2. Update \`tabBarLabel\` Text Style (Optional)\*\*

You also have \`paddingHorizontal: 5\` applied directly to the
\`\<Text\>\` element in your \`tabBarLabel\`. If you want the underline
to perfectly match the letters without any extra overhang, remove that
padding as well:

\`\`\`javascript

tabBarLabel: ({ focused, color, children }) =\> (

\<Text

style={{

color,

fontSize: 15,

fontFamily: focused ? theme.fonts.families.bold :
theme.fonts.families.regular,

fontWeight: focused ? \'700\' : \'400\',

textTransform: \'none\',

// paddingHorizontal: 5, \<\-- Remove this if you want it exactly the
length of the word

}}

\>

{children}

\</Text\>

),

\`\`\`

\*\*Why this works:\*\* React Navigation dynamically calculates the
width of the underline based on the container\'s width. By using margins
instead of padding, you push the tabs apart while keeping the container
width identical to your text width!

### **🔎 Why?**

Earlier (from your previous version), you had:

tabBarIndicatorStyle: {

transform: \[{ scaleX: 0 }\],

}

That line was **hiding the indicator completely**.

By removing that and replacing it with:

backgroundColor + height

# Problem 8

## **In the screen where we can select skills**

**src/components/forms/MultiSelectAutocompleteField.tsx**

### **The Problem**

Originally, the component had a few UX and technical gaps:

- **Navigation Trap:** The modal lacked a clear way to exit after
  selecting skills, as there was no \"Done\" action or auto-close
  mechanism.

- **Friction for Multi-Selection:** If the modal auto-closed after every
  tap, selecting multiple skills (like 5 or 8) became tedious for the
  user.

- **State \"Leftovers\":** If a user searched for a skill and closed the
  modal, that text would still be in the search bar when they reopened
  it.

- **Performance:** Large lists of skills could potentially cause
  scrolling lag without optimization.

### **The Solution**

We implemented a professional multi-select pattern in
MultiSelectAutocompleteField.tsx:

- **handleCloseModal Helper:** Created a single function that cleans up
  the state (clears search text), dismisses the keyboard, and hides the
  modal.

- **Non-Blocking Selection:** Modified addSkill to **not** close the
  modal automatically. This allows users to tap multiple skills and see
  the checkmarks appear in one session.

- **FlatList Optimization:** Added initialNumToRender,
  maxToRenderPerBatch, and windowSize to ensure the list remains buttery
  smooth regardless of the number of skills.

- **Header Refinement:** Replaced the generic \"X\" with a \"Check\"
  icon to signal a \"Done/Confirm\" action.

### **Why the \"Tick Mark\" (Check) is the Right Choice**

In this specific implementation, using a **Tick Mark** alone is superior
to an \"X\" or a combination for three reasons:

1.  **Instant State Persistence:** In your code, onChange is called the
    moment a skill is tapped. The data is already \"saved\" in the form
    state. A \"Tick\" accurately represents \"I am finished with my
    selections,\" whereas an \"X\" usually implies \"Cancel/Discard,\"
    which would be lying to the user since their taps were already
    recorded.

2.  **Clear Intent:** Since the modal allows for multiple selections,
    the \"Tick\" acts as a definitive \"Confirm\" button. It tells the
    user, \"Click this when you are satisfied with the list you\'ve
    built.\"

3.  **Visual Simplicity:** Adding both an \"X\" and a \"Tick\" creates a
    cluttered header and can confuse users about which one to press if
    they both essentially perform the same handleCloseModal function.
    The \"Tick\" provides a single, positive path forward.

**//why not use Save or Cancel buttons instead of Tick Mark**

In the context of a mobile \"Select Skills\" screen, using a **Tick
Mark** alone is generally better than separate **Save** or **Cancel**
buttons for the following reasons:

### **1. Mobile-First Design**

- On mobile devices, screen real estate is limited. A simple icon (the
  Tick) in the header is a standard design pattern that keeps the
  interface clean and focuses the user\'s attention on the search bar
  and the list of skills.

### **2. Reduced Decision Fatigue**

- \"Save\" and \"Cancel\" present a binary choice that forces the user
  to think: *\"Wait, did I change something I didn\'t mean to?\"*
  Because your code updates the selection instantly upon tapping a
  skill, a single \"Done\" (Tick) action is more honest---it simply
  tells the app, \"I\'m finished with this view\".

### **3. Avoiding the \"False Cancel\" Trap**

- In your current implementation, if you had a **Cancel** button, it
  would be technically misleading. Since the skills are added to the
  form state as soon as they are tapped, clicking \"Cancel\" wouldn\'t
  actually \"undo\" those taps---it would just close the modal. This can
  frustrate users who expect a Cancel button to roll back their changes.

### **4. Faster Workflow**

- A Tick mark in the top corner is a \"quick-exit\" point. For a user
  selecting 8+ skills, they want to get in, tap their skills, and get
  out. Having to look for a specific \"Save\" button at the bottom of a
  long list or in a different part of the header adds a tiny amount of
  friction that the Tick mark avoids.

- 

- **In short:** The Tick mark is a \"Confirmation\" rather than a
  \"Command.\" It confirms the user is happy with their current
  selection and wants to return to the main form.

- Would you like me to show you how to move the Tick mark to the right
  side of the header if you feel it\'s more reachable for the user\'s
  thumb?

# Problem 9

**File Modified:** SettingsScreen.tsx

### **The Problem**

The \"Settings\" menu contained broken, outdated, or placeholder actions
for essential legal documents. Specifically, clicking the \"Terms\" and
\"Privacy\" options only triggered placeholder toast messages instead of
routing the user to the actual policy web pages. You needed a way to
make these menu items functional so they could accept and open external
URLs.

### **The Solution Explanation**

To resolve this, we integrated React Native\'s native Linking API.

First, we added Linking to the React Native imports. Then, we created an
asynchronous helper function called handleOpenLink inside the component.
This function takes a URL string as an argument. Before blindly trying
to open the web page, it uses Linking.canOpenURL to verify that the
device actually supports opening that specific link. This is a crucial
safety check that prevents the app from crashing.

If the device supports the link, it uses Linking.openURL to launch it in
the user\'s default web browser. If it fails or is unsupported, it
triggers the existing error toast. Finally, we updated the onPress
events for the Terms and Privacy SettingItem components to trigger this
new function and pass in the target URLs.

### **The Code**

Here are the specific additions and modifications made to your file to
implement this solution:

**1. Import the API:**

TypeScript

import {

// \... other imports

Linking,

} from \'react-native\';

**2. The Helper Function:**

*(Added inside the SettingsScreen component)*

TypeScript

const handleOpenLink = async (url: string) =\> {

try {

const supported = await Linking.canOpenURL(url);

if (supported) {

await Linking.openURL(url);

} else {

toast.error(t(\'error\'));

}

} catch (err) {

console.error(\'An error occurred\', err);

toast.error(t(\'error\'));

}

};

**3. The Updated UI Components:**

*(Updated the onPress props in the About Section)*

TypeScript

{/\* About Section \*/}

\<Text
style={styles.sectionTitle}\>{t(\'settingsScreen.about\')}\</Text\>

\<View style={styles.section}\>

\<SettingItem

title={t(\'settingsScreen.terms\')}

onPress={() =\> handleOpenLink(\'https://yourcompany.com/terms\')}

icon=\"file-document-outline\"

/\>

\<SettingItem

title={t(\'settingsScreen.privacy\')}

onPress={() =\> handleOpenLink(\'https://yourcompany.com/privacy\')}

icon=\"shield-account-outline\"

showDivider={false}

/\>

\</View\>

# Problem 10

### **The Problem**

When a user taps the upvote or downvote button on a feed card, the card
abruptly jumps to a new position (either the top or bottom) in the feed
list. It gives the user the false impression that the post was removed,
dismissed, or that an error occurred, leading to a confusing and jarring
user experience. The expected behavior is that the card remains exactly
where it is, and only the vote count number updates.

### **The Cause of the Problem**

The root cause of this jumping behavior is a combination of **how your
frontend handles the vote success** and **how your backend sorts the
feed data.** Here is the exact step-by-step breakdown of why this
happens:

**1. The Trigger: Calling refresh() on Success**

In your PostCard component, when a user clicks the vote button, you
trigger the usePostVote API call. Inside the onSuccess callback of that
API request, you have this block of code:

JavaScript

if (typeof refresh === \'function\') {

refresh();

}

This refresh prop is actually the refetch function passed down from the
useUserFeed hook in your parent Feed.tsx file.

**2. The Full Feed Reload**

Because you call refresh(), the moment a vote is successfully
registered, your frontend tells the backend: *\"Hey, give me the entire
feed list all over again.\"*

**3. The Backend Sorting Logic**

When the backend receives this new request for the feed, it queries the
database. Most social or community feeds sort posts dynamically based on
an algorithm---usually prioritizing recent activity, engagement, or
total vote count. Because the post was just upvoted or downvoted, its
\"score\" or \"last active\" timestamp has changed.

**4. The FlatList Re-render (The \"Jump\")**

The backend sends the newly sorted list back to your frontend. The voted
post now has a brand new rank in that list. The FlatList in Feed.tsx
receives this new array of data and immediately re-renders to reflect
the new order. Because the post\'s index in the array has changed from
the backend, the FlatList instantly moves the card to its new position,
causing the visual \"jump.\"

### **Summary**

In short: **You are doing a full page refresh on a micro-interaction.**
Every vote forces the entire list to re-download and re-sort according
to the backend\'s algorithms. To keep the card in place, we have to
break that cycle by handling the vote UI updates locally
(optimistically) and trusting the backend to register the vote silently
in the background, without asking for the whole list back.

Would you like to move forward with implementing the optimistic update
code I provided earlier, or would you like to explore applying this same
fix to the \"Follow\" button logic first?

**SOLUTION:**

### **The Problem**

When a user tapped the upvote or downvote button on a post, the feed
card would abruptly jump to a new position (top or bottom) within the
list. This created a jarring user experience, making it look like the
post was dismissed or that a glitch occurred. The expected behavior was
for the card to stay exactly in place while only the vote count number
updated.

### **The Cause & Files Involved**

This issue spanned across two files, but the root cause lived in
**PostCard.tsx**.

1.  **The Trigger (PostCard.tsx):** Inside your postActionClick
    function, you had an API mutation (handlePostMutate) to send the
    vote to the server. Inside its onSuccess callback, you were calling
    a refresh() function.

2.  **The Chain Reaction (Feed.tsx):** That refresh() function was
    actually the refetch method passed down from the useUserFeed hook in
    the parent Feed.tsx file.

3.  **The Jump:** Calling refresh() forced the FlatList to re-download
    the entire feed. The backend returned the feed newly sorted (likely
    based on engagement/votes). The FlatList instantly re-rendered the
    array with the post\'s new index, causing the card to \"jump.\"

**The problematic code in PostCard.tsx looked like this:**

JavaScript

// BEFORE

handlePostMutate(

{ postId: post.id, value: voteValue },

{

onSuccess: () =\> {

AnalyticsService.trackEvent(\'post_vote\', {\...});

if (typeof refresh === \'function\') {

refresh(); // 🚨 This triggered the full list reload and the jump!

}

},

}

);

### **The Solution: Optimistic Updates**

To fix this, you modified **PostCard.tsx** to use a pattern called
**Optimistic UI Updates**. This means you update the UI instantly on the
device, trusting the server call will succeed in the background, and you
completely stop asking the server for a fresh list.

Here are the specific code parts you changed in PostCard.tsx:

**1. Added Local State:**

Instead of relying strictly on the props passed down from the server,
you created local state to track the vote visuals.

JavaScript

const \[localIsLiked, setLocalIsLiked\] = useState(initialIsLiked);

const \[localIsDisliked, setLocalIsDisliked\] =
useState(initialIsDisliked);

const \[localUpvotes, setLocalUpvotes\] = useState(initialUpvotes);

**2. Updated State Instantly:**

Inside the postActionClick function, you added math to instantly
calculate the new vote counts and toggle the arrow colors before the API
call even fires.

JavaScript

// Inside postActionClick

setLocalIsLiked(newIsLiked);

setLocalIsDisliked(newIsDisliked);

setLocalUpvotes(newUpvotes);

**3. Removed the refresh() Call:**

You stripped out the refresh() trigger from the onSuccess block. Now,
the API registers the vote silently in the background, and the FlatList
never re-renders the sorting order.

JavaScript

// AFTER

handlePostMutate(

{ postId: post.id, value: voteValue },

{

onSuccess: () =\> {

AnalyticsService.trackEvent(\'post_vote\', {\...});

// ✅ refresh() is gone! The card stays right where it is.

},

onError: () =\> {

// ✅ Added a fallback to revert the UI if the network request actually
fails

setLocalIsLiked(localIsLiked);

setLocalIsDisliked(localIsDisliked);

setLocalUpvotes(localUpvotes);

}

}

);

**4. Bound the JSX to Local State:**

Finally, you swapped out the old isLiked variables in your bottom action
bar UI for the new localIsLiked, localIsDisliked, and localUpvotes
variables so the buttons actually reflect the instant changes.

# Problem 11

**2 api endpoints problem:**

Here are the exact API endpoints based on your logs:

1.  **List API (Used for the parent cards i.e CommunityCard.tsx):** GET
    /communities/user/{userId}?sort=active (e.g.,
    /communities/user/264?sort=active)

2.  **Detail API (Used for the detail screen i.e CommunityDetail.tsx):**
    GET /communities/{communityId} (e.g., /communities/332)

**What to tell the backend team:**

You can copy and paste this directly to them:

\"Hey team, we have a data inconsistency between the Community List API
and the Community Detail API.

Currently, the Detail API (GET /communities/{id}) returns both
description and short_description. However, the List API (GET
/communities/user/{userId}) only returns description and is missing the
short_description field entirely.

Could you please update the List API so that each community object in
the response also includes the short_description field? I need this to
display the short description correctly on the community cards.\"

# Problem 12

Here is the updated summary, now including the API endpoint details and
the data structure you worked with:

### **Problem Statement**

The goal was to update the \"About\" tab in the Community Details screen
to display a new \"Community Type\" metric alongside the existing \"Max.
Members\" metric. The UI requirement dictated that these two metrics
needed to be displayed side-by-side in a two-column layout, mirroring a
specific design mockup. Additionally, the \"Community Type\" data needed
to be dynamically mapped from the privacy field in the existing API
response.

### **Solution**

1.  **Data Passing:** Updated the renderTabContent switch case in the
    parent component to extract the privacy field from the API data
    (communityInfo) and pass it down as a communityType prop.

2.  **Component Interface:** Expanded the About component\'s props
    definition to accept the new communityType string.

3.  **UI Layout Refactor:** Replaced the vertically stacked text
    elements at the bottom of the About component with a React Native
    View container utilizing flexDirection: \'row\'. Created two child
    View containers with flex: 1 to act as equal-width, 50/50 columns
    for \"Max. Members\" and \"Community Type\".

4.  **Styling:** Added corresponding flexbox styles (infoRow,
    infoColumn) and typography styles (infoTitle, infoText,
    capitalizeText) to format the labels and values accurately.

### **API Integration Details**

- **Endpoint:** GET /communities/{communityId} (e.g., /communities/332)

- **Relevant Response Data:** The component utilized the max_members and
  privacy fields from the JSON response object to populate the UI.

**Sample API Payload (Abridged):**

JSON

{

\"id\": \"332\",

\"name\": \"Kolkata II\",

\"description\": \"Kolkata Community Description\",

\"max_members\": 100,

\"privacy\": \"public\",

\"totalMembers\": 3,

\"membership\": {

\"is_member\": true,

\"status\": \"active\",

\"role\": null

}

}

### **Files Modified**

- **CommunityDetail.tsx**: Updated the renderTabContent function
  (specifically the \'About\' case) to pass the communityType prop to
  the \<About /\> component.

- **About.tsx**: Updated the component props, refactored the JSX to
  include the new flex-row layout, and added the required side-by-side
  styling to the AboutCommunityDetails stylesheet.

//To access the developer menu and the Toggle Inspector on your
connected Android device, use one of these two methods:

- **Shake the device:** Give your physical phone a gentle shake. This is
  the default hardware trigger to open the React Native developer menu.

- **Use your terminal:** If shaking doesn\'t work or you prefer keeping
  your hands on the keyboard, open your terminal and run:\
  **adb shell input keyevent 82**

# Problem 13

**///OTP VALUE HIDDEN UI ISSUE** in
**src/screens/founder/auth/authStyles.ts**

The dark-mode screenshot you shared clearly shows the 6th input box
completely cut off and the 5th box partially hidden. This is a classic
\"overflow\" layout error.

Here is the comparison between your original logic and the fixed logic.

**1. The Original Code (Causing the Issue)**

The problem was that the total width of the inputs plus the fixed gaps
was greater than the physical screen width of smaller devices.

TypeScript

// From your original authStyles.ts

verificationInputContainer: {

flexDirection: \'row\',

justifyContent: \'space-between\',

gap: theme.spacing.md, // Problem 1: Fixed physical gap (e.g., 16px)

marginTop: theme.spacing.lg,

marginBottom: theme.spacing.md,

paddingHorizontal: theme.spacing.md, // Problem 2: Takes up side space

},

otpInput: {

width: 45, // Problem 3: Fixed pixel width (won\'t shrink)

height: 45,

// \... rest of styles

},

**2. The New Code (The Fix)**

This version uses percentage-based widths and flexible spacing to ensure
it fits any screen.

TypeScript

// Your modified authStyles.ts

verificationInputContainer: {

flexDirection: \'row\',

justifyContent: \'space-between\', // Solution 1: Distributes extra
space automatically

marginTop: theme.spacing.lg,

marginBottom: theme.spacing.md,

width: \'100%\', // Solution 2: Uses the full available width of the
container

},

otpInput: {

width: \'14%\', // Solution 3: Mathematically guaranteed to fit 6 boxes
(14% \* 6 = 84%)

aspectRatio: 1, // Solution 4: Keeps boxes perfectly square as they
scale

borderRadius: theme.borderRadius.md,

backgroundColor: theme.colors.surface,

textAlign: \'center\',

fontSize: fontSizes.xl,

color: theme.colors.text,

fontFamily: fontFamilies.bold,

borderWidth: 1,

borderColor: theme.colors.border,

},

**The Problem Explained**

On a small device (like your teammate\'s), the screen might only be
**320px** wide.

- **Calculation:** If you have 6 boxes at **45px** each (\$270px\$) + 5
  gaps at **16px** (\$80px\$) + side padding of **32px**, you need a
  total of **382px**.

- **Result:** Since the screen is only 320px, the remaining 62px of your
  UI (the last box and a half) gets pushed off the right edge of the
  screen.

**The Solution Explained**

1.  **Removing gap:** By removing the fixed gap and using
    justifyContent: \'space-between\', you tell the phone to make the
    gaps as small as they need to be to fit the boxes on the screen.

2.  **Using Percentage (14%)**: This makes the boxes \"elastic.\" On a
    large emulator, they might be 50px wide; on a small phone, they
    might shrink to 38px wide. They will always adjust to the screen
    size.

3.  **aspectRatio: 1**: This ensures that when the width shrinks to fit
    the screen, the height shrinks by the same amount so the boxes
    don\'t look like tall, skinny rectangles.

# Problem 14

**The Problem:** After users successfully signed in with Google, they
were unable to edit their automatically fetched name to something more
professional because the text input field on the frontend was locked.

**The File:**

The UI code for this specific screen is located at:

src/screens/founder/auth/components/dataimport/PersonalDataStep.tsx

*(Note: We traced this from the main form wrapper DataImport.tsx through
the index.tsx bridge file in the same folder).*

**The Code Causing the Issue:**

Inside PersonalDataStep.tsx, the FormInput component responsible for
rendering the \"Full Name\" field had a hardcoded property locking it
down:

JavaScript

\<FormInput

config={{

type: \'text\',

control,

name: \'fullName\',

// \...

disabled: true, // \<\-\-- THIS WAS THE ISSUE

// \...

}}

/\>

**The Solution:**

Simply delete the disabled: true line (or change it to false) for the
fullName input. This unlocks the field, allowing the user to type a new
name, which your existing backend logic in DataImport.tsx will
automatically capture and save.

# Problem 15

## **Summary of Task and Solution**

### **File Name**

The code you modified is located in **Events.tsx**.

### **Original Problem Statement**

The primary issue involved the **Thumbnail Image Position Alignment**
within the event cards. The original UI caused the thumbnail image to
align strictly with the top-left, which resulted in **excessive padding
at the bottom** of the card when the text content (title, location, and
dates) was shorter than the image height. The goal was to:

- Ensure the image is set properly without using unnecessary padding
  adjustments.

- Keep the positioning visually consistent regardless of whether the
  location text is a single line or two lines.

- Prevent future layout issues by making the alignment robust.

### **Code Snippet Solution**

To solve this, you implemented a more balanced layout within the
EventsStyles and JSX structure:

- **Vertical Centering:** You changed the eventCard container to
  alignItems: \'center\', which ensures the thumbnail stays centered
  relative to the text block even if the text height changes.

- **Scaled Dimensions:** You increased the thumbnail dimensions in
  cardImageWrap to **\$125 \\times 125\$** with a **16px** border radius
  to better match the visual weight of the card.

- **Content Density:** By keeping the **Date** and **Time** containers
  stacked vertically rather than putting them on one line, you increased
  the height of the right-hand text section. This naturally fills the
  vertical space next to the image, effectively eliminating the
  \"excessive padding\" issue mentioned in the task.

# Problem 16

**Event Creation Flow:**\
While trying to create an event on the event page, I encountered an
issue. After filling in all the details and clicking the \'Create
Event\' button, it unexpectedly shows an \'Are you sure you want to
close this?\' popup. This confirmation popup should only appear when
clicking the \'X\' (close) icon at the top, not on the submit button.
Please look into this bug.\
But events are getting created.\
\
**Screenshot:**
[[https://ibb.co/qYHdHk1y]{.underline}](https://ibb.co/qYHdHk1y)

[[https://ibb.co/XfcsW4WV]{.underline}](https://ibb.co/XfcsW4WV)

## **The Problem: The \"Aggressive\" Navigation Guard**

### **The Symptom**

When you clicked \"Create Event,\" the event would successfully be
created in the database, but the app would stay on the form page and
show a **\"Discard Event?\"** popup.

### **The Cause**

You had a beforeRemove listener designed to prevent users from
accidentally losing their work. However, this listener couldn\'t tell
the difference between a user **canceling** and a user **successfully
submitting**. It saw \"unsaved changes\" (the text in the inputs) and
blocked the navigation regardless of the button pressed.

### **The Buggy Snippet (CreateEvent.tsx)**

The original code lacked a \"pass\" for successful submissions and used
useState, which was too slow to update before the navigation fired.

TypeScript

// PROBLEM: No way to bypass the guard on success

useEffect(() =\> {

const unsubscribe = navigation.addListener(\'beforeRemove\', (e) =\> {

const values = getValues();

const hasUnsavedChanges = values.title \|\| values.description; //
etc\...

if (!hasUnsavedChanges) return;

// This always fired because the form was \"dirty\"

e.preventDefault();

setIsDiscardDialogVisible(true);

});

return unsubscribe;

}, \[navigation, getValues\]);

## **The Solution: The \"Success Pass\" with useRef**

### **The Fix**

We introduced a **Ref** (isSuccessfullySubmittedRef). Unlike useState, a
**Ref** updates instantly. We set this to true the moment the API
returns a success, allowing the navigation guard to let you pass through
without showing the popup.

### **The Corrected Snippets (CreateEvent.tsx)**

**1. The Setup**

TypeScript

const isSuccessfullySubmittedRef = useRef(false);

**2. The Guard Logic**

We added a check at the very top of the listener to see if we are
leaving because of a success.

TypeScript

useEffect(() =\> {

const unsubscribe = navigation.addListener(\'beforeRemove\', (e) =\> {

// SOLUTION: If we succeeded, ignore the unsaved changes and let them
go!

if (isEdit \|\| isSuccessfullySubmittedRef.current) {

return;

}

// \... rest of the guard logic

});

return unsubscribe;

}, \[navigation, isEdit, getValues, eventImage\]);

**3. The Submit Logic**

We update the Ref immediately before navigating back.

TypeScript

onSubmit: () =\> {

createEventMutate(payload, {

onSuccess: () =\> {

// SOLUTION: Flip the switch to \'true\' instantly

isSuccessfullySubmittedRef.current = true;

navigation.goBack();

},

});

}

## **Files Involved**

1.  **CreateEvent.tsx**: This is where the actual bug and fix lived. It
    handles the form logic and the navigation guard.

2.  **Events.tsx**: This is the list view. It was working correctly, but
    we verified that it now properly shows the new event card once the
    CreateEvent screen closes.

Now that your event creation flow is smooth, **would you like me to help
you implement a \"Pull to Refresh\" or a \"Success Toast\" so the user
gets better feedback when the event is added?**

### **📝 Note -- Import Path Change for Local Wireless Debugging**

For local wireless debugging on macOS (React Native CLI), I changed the
import in App.tsx:

import \'@/i18n\';

to

import \'./src/i18n\';

Reason:\
Metro bundler failed to resolve the @/i18n alias during wireless
debugging and returned a 500 error (UnableToResolveError). Using the
relative path ensures proper module resolution without relying on alias
configuration.

This change only affects module import syntax and does not modify
functionality.

Now your second question:

> are these 2 statements the same thing?

import \'@/i18n\';

and

import \'./src/i18n\';

### **✅ Conceptually --- Yes**

Both are trying to import the same file.

### **❌ Technically --- Not Always**

They are the same **only if** your alias @ is correctly configured to
point to src.

If alias is configured properly:

@ → ./src

Then:

@/i18n === ./src/i18n

If alias is misconfigured (like in your case), then they are NOT the
same.

### **🔥 Simple Rule**

- ./src/i18n → always works (plain relative path)

- @/i18n → works only if alias setup is correct in:

  - babel.config.js

  - tsconfig.json

  - metro configuration (if needed)

# Problem 17

![](data/media_dump/media/image11.png){width="5.880208880139983in"
height="4.636317804024497in"}

Note:

Every single change we made was directly driven by the \"Feed, Explore &
Trending\" frontend implementation guide you uploaded.

Here is exactly how our solutions map directly to the rules in that
document, with the specific file names included:

- **The Pagination Fixes (updating
  src/api/services/discussion.service.ts,
  src/api/hooks/useDiscussion.ts, and Feed.tsx):** This directly
  satisfies the \"Pagination (Cursor-Based)\" section of the document.
  The guide explicitly states that the feed uses cursor-based
  pagination, not page numbers, to ensure stable scrolling with no
  duplicate or missing posts. It also dictates that the frontend must
  always use the next_cursor value returned by the API.

- **The Voting Fix (removing refresh() in
  src/screens/community/components/common/PostCard.tsx):** This
  addresses the section literally named \"CRITICAL: Frontend Behavior
  After Voting\". The document has a strict rule: \"Do NOT re-fetch the
  feed API after a vote\". It specifically warns that if the frontend
  re-fetches the feed after a vote, the backend will exclude the
  just-voted post, and the card will disappear instantly---this is
  confusing and was reported as a bug by testers.

- **Optimistic UI Updates (managing local state in
  src/screens/community/components/common/PostCard.tsx):** The guide
  requires the frontend to update the card\'s vote count locally in
  state (optimistic update) and keep the card in its current position on
  the list. Our local state variables in PostCard.tsx achieved exactly
  this.

### **\[Ankita Problem\] Feed API Pagination & Optimistic Voting UI Bug**

**Problem Description:** The frontend feed implementation was violating
two major backend contracts. First, it lacked the required cursor-based
pagination, resulting in only a single page of posts loading. Second,
upvoting, downvoting, or following a user triggered a full feed
refetch(). The backend explicitly forbids re-fetching after a vote.
Because the backend filters out voted posts on a fresh load, this causes
the posts to instantly disappear from the user\'s screen, creating a
jarring UX.

**Solution Strategy:** Implemented useInfiniteQuery to handle cursor
parameters, flattened the incoming pages into a deduplicated array, and
stripped out all forced feed refetches after mutations in favor of
optimistic local state updates.

### **Files Changed & Code Snippets**

#### **1. src/api/services/discussion.service.ts**

**Change:** Updated the API service function to accept and pass query
parameters (limit and cursor) to the backend.

TypeScript

// Changed from: export const UserFeed = async () =\> \...

export const UserFeed = async (params?: any) =\>

await apiClient.get(API_ENDPOINTS.DISCUSSION.USER_FEED, { params });

#### **2. src/api/hooks/useDiscussion.ts**

**Change:** Swapped useQuery for useInfiniteQuery to support fetching
sequential pages using the next_cursor provided by the backend response.

TypeScript

// Replaced standard useQuery block with:

export const useUserFeed = (params?: any) =\>

useInfiniteQuery({

queryKey: \[queryKeys.discussion.userFeed, params\],

initialPageParam: null,

queryFn: ({ pageParam }) =\>

UserFeed({ \...params, \...(pageParam ? { cursor: pageParam } : {}) }),

getNextPageParam: (lastPage: any) =\> {

const pagination = lastPage?.data?.data?.pagination \|\|
lastPage?.data?.pagination;

if (pagination?.has_more) {

return pagination.next_cursor;

}

return undefined;

},

});

#### **3. Feed.tsx (Inside src/screens/community/components/community-dashboard/TabScreen/)**

**Change:** Extracted infinite scroll methods, safely flattened and
deduplicated the pages array to avoid React key errors, removed the
refresh={refetch} prop from PostCard, and wired up onEndReached on the
FlatList.

TypeScript

// 1. Updated Hook

const { data: userFeedData, isFetching, refetch, fetchNextPage,
hasNextPage, isFetchingNextPage } = useUserFeed({ limit: 10 });

// 2. Flattened & Deduplicated Data

const FeedData = React.useMemo(() =\> {

if (!userFeedData?.pages) return \[\];

const allItems = userFeedData.pages.flatMap((page: any) =\> {

return pathOr(null, \[\'data\', \'data\', \'items\'\], page) \|\|
pathOr(\[\], \[\'data\', \'items\'\], page);

});

return Array.from(new Map(allItems.map((item: Post) =\> \[item.id,
item\])).values());

}, \[userFeedData\]);

// 3. Removed refresh prop from PostCard

const renderPost = React.useCallback(

({ item }: { item: Post }) =\> (

\<PostCard

post={item}

handlePostClick={(postId: string) =\> {
navigation.navigate(\'CommunityPostDetail\', { postId }); }}

// refresh={refetch} \<\-- REMOVED

/\>

), \[navigation\]

);

// 4. Added to FlatList props

\<FlatList

// \...

onEndReached={() =\> {

if (hasNextPage && !isFetchingNextPage) fetchNextPage();

}}

onEndReachedThreshold={0.5}

ListFooterComponent={isFetchingNextPage ? \<Text\>Loading
more\...\</Text\> : null}

/\>

#### **4. src/screens/community/components/common/PostCard.tsx**

**Change:** Removed the refresh() calls from both the vote and follow
mutation onSuccess callbacks. The component now correctly relies
entirely on its local useState variables for optimistic UI updates.

TypeScript

// Inside postActionClick -\> handlePostMutate:

handlePostMutate(

{ postId: post.id, value: voteValue },

{

onSuccess: () =\> {

AnalyticsService.trackEvent(\'post_vote\', { \... });

// REMOVED: refresh() call. Card stays in place.

},

// \...

}

);

// Inside Follow Button TouchableOpacity -\> onPress:

handleFollowUserMutate(UserUUID, {

// REMOVED: onSuccess: () =\> { refresh(); }

})

# Problem 18

Here is a complete summary of the problem and the fix based on our
discussion:

### **Problem Summary**

When viewing another user\'s profile, normal users and founders were
unable to click the \"Connections\" or \"Followers\" text to view the
network lists. The text appeared in white (instead of the primary yellow
hyperlink color) and nothing happened when clicked. Also this problem
wasn't occurring if the user account was an investor.

**Note:** There was no backend API error to begin with. The backend was
fully capable of returning this data for any user. The issue was
entirely a frontend UI restriction preventing the navigation from
triggering in the first place.

### **Root Cause**

The issue originated in **UserProfileCard.tsx**. The UI was
intentionally coded to enforce a \"private network\" view. It restricted
access by checking if the logged-in user was either the profile owner
(isOwner) or already connected to the user (isConnected).

If those conditions weren\'t met, the code did three things:

1.  Disabled the TouchableOpacity component completely.

2.  Blocked the navigation.navigate action inside the onPress event.

3.  Swapped the text color from the primary hyperlink color to the
    default text color.

**The Original Restrictive Code (Snippet):**

JavaScript

// Inside UserProfileCard.tsx

\<TouchableOpacity

activeOpacity={0.7}

disabled={!isOwner && !pathOr(false, \[\'isConnected\'\],
UserProfileData)} // 1. Blocked clicks

onPress={() =\> {

if (isOwner) {

navigation.navigate(SCREEN_NAMES.MY_CONNECTIONS);

} else if (pathOr(false, \[\'isConnected\'\], UserProfileData)) { // 2.
Blocked navigation

navigation.navigate(SCREEN_NAMES.USER_CONNECTIONS, { \... });

}

}}

\>

\<Text style={\[styles.userNetworkText, {

color: isOwner \|\| pathOr(false, \[\'isConnected\'\], UserProfileData)

? theme.colors.primary

: theme.colors.text // 3. Hid the hyperlink color

}\]}

\>

{networkStats?.totalConnections ?? 0} Connections

\</Text\>

\</TouchableOpacity\>

### **The Fix**

To allow all account types (normal users, founders, and investors) to
freely click and view the network lists, the relationship-based gates
were stripped from the UI.

**File Modified:** UserProfileCard.tsx (This was the *only* file needed
to fix the issue).

**The Changes Made:**

1.  Deleted the disabled prop entirely.

2.  Removed the else if (isConnected) check, leaving a simple else
    fallback so anyone who isn\'t the owner gets routed to the
    USER_CONNECTIONS screen.

3.  Hardcoded the text color to always use theme.colors.primary.

**The Fixed Code (Snippet):**

JavaScript

// Inside UserProfileCard.tsx

\<TouchableOpacity

activeOpacity={0.7}

// No more disabled prop

onPress={() =\> {

if (isOwner) {

navigation.navigate(SCREEN_NAMES.MY_CONNECTIONS);

} else { // Unrestricted navigation

navigation.navigate(SCREEN_NAMES.USER_CONNECTIONS, {

userId: pathOr(\'\', \[\'id\'\], UserProfileData),

type: \'connections\',

userName: pathOr(\'\', \[\'fullName\'\], UserProfileData),

});

}

}}

style={{ flexDirection: \'row\', alignItems: \'center\' }}

\>

\<Text

style={\[

styles.userNetworkText,

{ color: theme.colors.primary }, // Permanently set to primary color

\]}

\>

{networkStats?.totalConnections ?? 0} Connections

\</Text\>

\</TouchableOpacity\>

*(The exact same changes were applied to the Followers button directly
below it).*

# Problem 19

Here is a complete summary of the problems and the solutions we
implemented. You can save this as documentation for future reference!

\-\--

\# Bug Resolution Summary: React Native Community Creation Flow

\## 📌 The Problems

1\. \*\*404 API Error on Screen 3:\*\* Uploading an image directly on
the \`CommunitySummary\` screen threw a 404 error.

2\. \*\*Missing Image Upload from Screen 1:\*\* Selecting a community
icon on the \`AddCommunity\` screen didn\'t successfully attach to the
community or show up in the final review screen.

3\. \*\*Stuck Image Placeholder:\*\* Even after fixing the upload logic,
the image wouldn\'t render on Screen 3 because the component didn\'t
update after the API fetched the data.

\-\--

\## 🛠️ Solutions & Code Snippets

\### 1. Fixing the 404 Error on Screen 3

\*\*File:\*\* \`CommunitySummary.tsx\`

\*\*The Cause:\*\* The frontend was calling \`useUpdateCommunity\` (the
generic text-data update endpoint) and passing only an image and a
\`communityId\`. The backend rejected this partial payload/wrong route.

\*\*The Fix:\*\* Swapped the hook to use the dedicated image upload
hook: \`useUpdateCommunityIcon\`.

\*\*Code Fix:\*\*

\`\`\`tsx

// ❌ BAD: Used the generic update hook

// import { useUpdateCommunity } from \'../../api/hooks/useCommunity\';

// ✅ GOOD: Imported the dedicated icon update hook

import { useUpdateCommunityIcon } from \'../../api/hooks/useCommunity\';

const CommunitySummary = () =\> {

// \...

// ✅ Swapped mutation hook

const { mutate: handleCommunityUpdateIconMutate, isPending:
isUpdatingCommunityIcon } =

useUpdateCommunityIcon();

// \...

\<ImagePickerComponent

handleUploadImage={(image: string) =\> {

handleCommunityUpdateIconMutate(

{

communityId: communityId, // Payload structure matches the service
requirement

icon_url: image,

},

{ onSuccess: () =\> refetch() }

);

}}

initialImageUrl={ImageURL}

/\>

\`\`\`

\### 2. Fixing the Image Upload Chain in Screen 1

\*\*File:\*\* \`AddCommunity.tsx\`

\*\*The Cause:\*\* The local device image path (\`file://\...\`) was
being sent as a standard string inside the JSON payload for
\`useCreateCommunity\`. Backends usually require files to be sent to a
separate endpoint or via \`FormData\`.

\*\*The Fix:\*\* We chained the API calls. We first create the community
data -\> get the returned \`id\` -\> immediately fire
\`useUpdateCommunityIcon\` with that new ID -\> \*then\* navigate to the
next screen.

\*\*Code Fix:\*\*

\`\`\`tsx

import { useCreateCommunity, useUpdateCommunityIcon } from
\'../../api/hooks/useCommunity\';

const AddCommunity = () =\> {

const { mutate: createCommunityMutate } = useCreateCommunity();

const { mutate: uploadIconMutate, isPending: isUploadingIcon } =
useUpdateCommunityIcon(); // ✅ Added hook

const handleViewSummary = (data: CommunityFormData) =\> {

const payload = {

name: data?.name ?? \'\',

// \... other fields

\...(communityId && { communityId }), // ✅ Fixed key from \'id\' to
\'communityId\' to match API service

};

if (communityId) {

// \... Update logic

} else {

createCommunityMutate(payload, {

onSuccess: (response: any) =\> {

const newCommunityId = response?.data?.id;

// ✅ Chained Upload Logic: If image exists, upload it BEFORE navigating

if (data.icon_url) {

uploadIconMutate(

{ communityId: newCommunityId, icon_url: data.icon_url },

{

onSettled: () =\> {

navigation.navigate(SCREEN_NAMES.COMMUNITY_RULES, {

communityId: newCommunityId,

communityName: response?.data?.name,

});

},

}

);

} else {

// No image, navigate immediately

navigation.navigate(SCREEN_NAMES.COMMUNITY_RULES, { /\*\...\*/ });

}

},

});

}

};

// \... Remembered to add \`isUploadingIcon\` to the button\'s
loading/disabled props

\`\`\`

\### 3. Fixing the Stuck Image Placeholder (UI Render Bug)

\*\*File:\*\* \`CommunitySummary.tsx\`

\*\*The Cause:\*\* \`ImagePickerComponent\` relies on an
\`initialImageUrl\` prop. Because of the network delay when fetching
community details, this prop was initially an empty string \`\'\'\`.
When the API data arrived seconds later, the component ignored the new
value because it only reads \"initial\" props on its first render.

\*\*The Fix:\*\* Added a \`key\` prop tied to the fetched \`ImageURL\`.
In React, changing a component\'s \`key\` forces it to completely
unmount and remount, forcing it to read the newly fetched URL.

\*\*Code Fix:\*\*

\`\`\`tsx

const ImageURL = pathOr(\'\', \[\'data\', \'icon_url\'\],
fetchedCommunityData);

// \...

\<ImagePickerComponent

key={ImageURL} // ✅ Added this to force React to remount when API data
arrives

handleUploadImage={(image: string) =\> { /\*\...\*/ }}

initialImageUrl={ImageURL}

/\>

\`\`\`

\### 🎉 Summary of Key Takeaways:

\* \*\*API Payloads:\*\* Never assume a generic PUT/POST endpoint will
handle both JSON text strings and file uploads simultaneously unless
explicitly designed to do so (like with \`multipart/form-data\`).

\* \*\*React Rendering:\*\* If a component with an \`initialValue\` prop
isn\'t updating after an API fetch, tying a dynamic \`key={data}\` to it
is the cleanest way to force a re-render.

\* \*\*API Service definitions:\*\* Always double-check what keys the
service file is destructuring (e.g., \`{ communityId }\` vs \`{ id }\`).

# Problem 20

Here is a complete summary of the problem and the solution that you can
add to your documentation for future reference:

# **Bug Resolution Summary: React Navigation Reset Crash on Role-Based Stacks**

## **📌 The Problem**

**Error:** The action \'RESET\' with payload
{\"index\":1,\"routes\":\[{\"name\":\"MainStack\"}\... was not handled
by any navigator.

**The Cause:** The app uses conditional root navigators based on user
roles (MainNavigator for Founders/Normal users, and
MainInvestorNavigator for Investors). In the shared CommunitySummary
screen, the \"Go to Community\" button used a navigation.reset() action
that was hardcoded to route to STACK_NAMES.MAIN. When an Investor
clicked this button, the app crashed because STACK_NAMES.MAIN does not
exist in their specific navigation tree.

**Secondary Issues:** 1. **TypeScript Strictness:** Using Ramda\'s
pathOr to default to \'Founder\' caused TypeScript to strictly infer the
literal type \"Founder\", throwing a ts(2367) error when trying to
compare it to \'Investor\'.

2\. **Duplicate Params:** There was an accidental duplicate name key
inside the route params object.

## **🛠️ The Solution**

**The Fix:** We made the navigation reset action dynamic. By pulling the
current user from the useAuthStore, we check their userType and assign
the correct root stack (STACK_NAMES.INVESTOR or STACK_NAMES.MAIN) before
triggering the reset. We also bypassed the TypeScript literal inference
by typing userType as any, and cleaned up the duplicate parameter.

**File Modified:** CommunitySummary.tsx

**Code Fix:**

TypeScript

// 1. Imported the Auth Store

import { useAuthStore } from \'@/store\';

const CommunitySummary = () =\> {

// 2. Extracted user from the store

const { user } = useAuthStore();

// \... other hooks \...

const handleDone = () =\> {

// 3. Extracted userType with \`: any\` to bypass strict TS literal
checking

const userType: any = pathOr(\'Founder\', \[\'userType\'\], user);

// 4. Checked role and dynamically set the root stack

const isInvestor = userType === \'Investor\' \|\| userType ===
\'investor\';

const rootStackName = isInvestor ? STACK_NAMES.INVESTOR :
STACK_NAMES.MAIN;

navigation.reset({

index: 1,

routes: \[

// 5. Replaced hardcoded STACK_NAMES.MAIN with the dynamic variable

{ name: rootStackName },

{

name: SCREEN_NAMES.COMMUNITY_DETAILS,

params: {

// 6. Removed the duplicate \`name\` key here

communityId: communityId,

communityName: pathOr(\'\', \[\'data\', \'name\'\],
fetchedCommunityData),

},

},

\],

});

};

// \... rest of component

# Problem 21

Here is a quick summary you can use for your commit message or QA ticket
response:

**File:** The file containing your AddCommunity component (likely
AddCommunity.tsx or AddCommunity.jsx).

- **Problem:** The invalidation icon for an already taken community name
  displays as a red plus sign (+) instead of an \"X\". This happens
  because the string \'cross\' passed to the icon library maps to a
  medical cross rather than a cancellation mark.

- **Solution:** Update the Community Name FormInput right-side icon from
  \'cross\' to \'close-circle\' to render the requested \"red circle
  enclosing an X\", or replace it with the specific asset provided by
  Souvik.

# Problem 22

Here is the complete summary of the bug and the specific code
transformations you implemented across the three affected files to
resolve the navigation, title, and performance issues.

**Page Title issue:**

The current page title for both the \'Follower\' and \'Connection\' list
views is confusing because it is identical to the underlying API
endpoint name, which is not user-friendly. To ensure a clearer and more
professional user experience across all applicable flows (Investor,
Founder, Member), the page titles must be renamed to be more descriptive
and user-facing. Specifically, the \'Connections List\' view, currently
titled by its API name, should be changed to \"Connections,\" and the
\'Followers List\' view should be changed to \"Followers.\" This is an
essential action to improve the overall usability of the application.

### **1. Navigation & UI Duplication**

**File:** UserProfileCard.tsx

**Problem:**

The component had two identical buttons that both sent the user to the
\"Connections\" view, regardless of which label was clicked.

#### **Changes Made**

**From (Old Logic):**

TypeScript

// Both buttons were effectively doing this:

navigation.navigate(SCREEN_NAMES.USER_CONNECTIONS, {

userId: pathOr(\'\', \[\'id\'\], UserProfileData),

type: \'connections\', // Hardcoded for both

userName: pathOr(\'\', \[\'fullName\'\], UserProfileData),

});

**To (New Logic):**

TypeScript

// Followers Button

navigation.navigate(SCREEN_NAMES.USER_CONNECTIONS, {

userId: pathOr(\'\', \[\'id\'\], UserProfileData),

type: \'followers\', // Now correctly identifies the intent

userName: pathOr(\'\', \[\'fullName\'\], UserProfileData),

});

// Connections Button

navigation.navigate(SCREEN_NAMES.USER_CONNECTIONS, {

userId: pathOr(\'\', \[\'id\'\], UserProfileData),

type: \'connections\',

userName: pathOr(\'\', \[\'fullName\'\], UserProfileData),

});

### **2. API Hook Flexibility**

**File:** useNetworkStats.ts

**Problem:** The hooks were hardcoded to only accept a userId. Passing
an enabled flag from the component caused a TypeScript error (\"Expected
1 arguments, but got 2\").

#### **Changes Made**

**From (Old Logic):**

TypeScript

export const useGetUserConnectionsList = (userId: string \| number) =\>

useQuery({

queryKey: \[queryKeys.connections.getUserConnectionsList, userId\],

queryFn: () =\> getUserConnectionsList(userId),

enabled: !!userId,

});

**To (New Logic):**

TypeScript

// Added \'options\' parameter and spread it into the useQuery call

export const useGetUserConnectionsList = (userId: string \| number,
options?: any) =\>

useQuery({

queryKey: \[queryKeys.connections.getUserConnectionsList, userId\],

queryFn: () =\> getUserConnectionsList(userId),

enabled: !!userId,

\...options, // Allows the component to override \'enabled\'

});

### **3. Performance & Page Title Logic**

**File:** UserConnections.tsx

**Problem:** Both API hooks were firing on every load, and the title
displayed raw translation keys (e.g., connections.userFollowers.title)
instead of human-readable text.

#### **Changes Made (API Fetching)**

**From (Old Logic):**

TypeScript

// Both ran simultaneously

const { data: connectionsResponse, \... } =
useGetUserConnectionsList(type === \'connections\' ? userId : \'\');

const { data: followersResponse, \... } = useGetUserFollowersList(type
=== \'followers\' ? userId : \'\');

**To (New Logic):**

TypeScript

// Only the relevant hook is \'enabled\' based on the navigation type

const { data: connectionsResponse, \... } =
useGetUserConnectionsList(userId, {

enabled: type === \'connections\' && !!userId

});

const { data: followersResponse, \... } =
useGetUserFollowersList(userId, {

enabled: type === \'followers\' && !!userId

});

#### **Changes Made (Title Logic)**

**From (Old Logic):**

TypeScript

const title = type === \'connections\'

? t(\'connections.userConnections.title\', { name: userName })

: t(\'connections.userFollowers.title\', { name: userName });

**To (New Logic):**

TypeScript

// Checks if the translation failed (returned the key) and applies a
fallback

const title = type === \'connections\'

? userName

? t(\'connections.userConnections.title\', { name: userName
}).includes(\'connections.\')

? \`\${userName}\'s Connections\`

: t(\'connections.userConnections.title\', { name: userName })

: t(\'connections.connectionsTitle\', \'Connections\')

: // \... repeat logic for followers

### **Final Result**

1.  **Correct Titles:** The header now shows **\"Mikasa\'s Followers\"**
    or **\"Mikasa\'s Connections\"** dynamically.

2.  **Optimized Speed:** The app no longer makes unnecessary network
    requests for the list you aren\'t viewing.

3.  **Clean Code:** TypeScript is satisfied, and the UI correctly
    reflects the user\'s intent.

# Problem 23

**//skeletonloader problem (previously thought it was schimmer effect
but it was not)**

Here is the step-by-step breakdown of exactly what happens when you open
the Search screen, from the bottom up.

Think of it like building a house: you have the raw materials, the
blueprint, and the final construction.

**The Structure (Chain of Imports)**

Here is how the files are connected:

1.  **SkeletonLoader.tsx** (The Raw Materials)

    - **What it does:** This file creates the basic gray shapes
      (circles, rectangles, and lines of text) and tells them to pulse
      their opacity up and down.

    - **What it exports:** Skeleton, SkeletonCircle, SkeletonText.

2.  **ListItemSkeleton.tsx** (The Blueprint)

    - **What it does:** This file imports the raw materials from
      SkeletonLoader.tsx. It takes a circle and places it on the left,
      takes some text lines and puts them on the right. It arranges the
      raw materials so they look exactly like an empty search result.

    - **What it exports:** ListItemSkeleton.

3.  **Search.tsx** (The Final Construction)

    - **What it does:** This is the actual screen you see. It imports
      ListItemSkeleton and decides *when* to show it to you.

**What Happens When You Open the Search Screen**

Here is the exact sequence of events the moment you tap on the Search
tab:

**Step 1: The Data Request Begins**

When the screen opens, the app immediately tries to fetch the initial
search data (or whatever you just typed) using your custom hooks
(useGetSearchedData or useGetSearchedDataInfinite).

**Step 2: The \"Loading\" Flag is Raised**

Because it takes a split second for the server to reply, a variable
inside Search.tsx called searchFetching becomes true. At this moment,
the variable searchData is still empty because nothing has arrived yet.

**Step 3: The Code Triggers the Shimmer**

Down at the bottom of your Search.tsx file, there is a specific rule:

JavaScript

if (searchFetching && !searchData) {

// Show the skeletons!

}

This translates to: *\"If we are actively fetching data AND we don\'t
have any data to show yet, do this next part.\"*

**Step 4: Drawing the List**

Inside that if statement, the app takes the ListItemSkeleton blueprint
and stamps it on the screen 8 times in a row:

JavaScript

{\[1, 2, 3, 4, 5, 6, 7, 8\].map(i =\> (

\<ListItemSkeleton key={\`skeleton-\${i}\`} /\>

))}

**Step 5: The Data Arrives (The Swap)**

A moment later, the server replies with the real people, companies, or
jobs. The searchData variable fills up, and searchFetching becomes
false.

Because the rule from Step 3 is no longer true, the 8 shimmering
skeletons instantly disappear, and the real \<FlatList\> with your
actual search results is drawn in their place.

**The Short Conclusion on the Shimmer**

The \"shimmer\" is actually a **pulsing opacity animation** powered by
your SkeletonLoader.tsx file.

In your Search screen, it works like a placeholder switch:

1.  You open Search, and the app asks the server for data.

2.  While waiting (searchFetching is true), the app renders the
    **ListItemSkeleton** component multiple times to mimic a list.

3.  The moment the data arrives, it flips the switch, unmounts the
    skeletons, and renders the real data.

You don\'t see this in some other tabs (like Home) because those screens
are built to use your \<Fallback /\> component (the animated \"CHIIRO\"
logo) as a blanket loading screen, rather than using these individual
list item skeletons.

**The Skeleton Files in Your Screenshot**

The screenshot reveals a really solid, highly modular UI pattern.
Instead of having one generic loading box, your app has a specific
\"ghost\" version of almost every UI component. This is excellent for
preventing layout shifts when the real data finally renders.

Here is what all those files are doing based on their names:

- **CommunityCardSkeleton.tsx**: The placeholder for community groups.
  It mimics a larger card layout (likely an avatar, a title, two lines
  of description, and a row of badges, as we saw in its code earlier).

- **ConnectionItemSkeleton.tsx**: The placeholder for the \"My Network\"
  or friends list (usually an avatar, name, and a \"Connect/Follow\"
  button placeholder).

- **ConversationItemSkeleton.tsx**: The placeholder for the chat/inbox
  screen. It likely features an avatar, a name, a snippet of the latest
  message, and a timestamp on the right.

- **EventCardSkeleton.tsx**: The placeholder for upcoming events,
  probably mimicking a date calendar block, event title, and location.

- **FeedItemSkeleton.tsx**: A larger, more complex skeleton for the main
  timeline (similar to a LinkedIn or Twitter post placeholder with a
  user header, body text blocks, and an image placeholder).

- **JobItemSkeleton.tsx**: The placeholder for the job board, mimicking
  a company logo, job title, and tags (like \"Remote\" or
  \"Full-time\").

- **ListItemSkeleton.tsx**: The generic list placeholder we looked at,
  used in places like the Search results.

- **ProfileSectionSkeleton.tsx**: Used on the User Profile screen to act
  as a placeholder for larger blocks of data, like the \"Experience\" or
  \"About\" sections.

- **SkillSkeleton.tsx**: A smaller placeholder specifically for the
  pill-shaped tags inside a user\'s skills section.

- **NotificationItemSkeleton.tsx**: The placeholder for the
  notifications screen, likely mimicking an avatar, a multi-line
  activity sentence, and an icon.

**Why This Matters**

All of these files act as the \"Blueprints\" for different screens, but
they all rely on the same \"Raw Materials\" from SkeletonLoader.tsx.
Because of this centralized architecture, if you ever want to change the
loading animation from a \"pulse\" to a \"left-to-right shimmer,\" you
only have to edit SkeletonLoader.tsx once, and it will instantly update
the loading states across your entire app---from the feed to the job
board.

Here are those two details formatted so you can easily copy and paste
them right into your summary:

**1. Add this to the \"The Structure\" section (under
ListItemSkeleton)**

**Customizing the Blueprints (Props)**

**Note on Flexibility:** These blueprints aren\'t completely rigid.
Components like ListItemSkeleton accept **props** (such as
showSearchIcon, circularAvatar, and avatarSize). This means you can
easily tweak the layout on the fly---like hiding the search icon or
changing a square avatar to a circle---without needing to build a brand
new skeleton file for every minor UI variation.

**2. Add this right after \"The Short Conclusion on the Shimmer\"**

**How to Tweak the Engine (SkeletonLoader.tsx)**

Because every skeleton relies on the central SkeletonLoader.tsx engine,
you can change the loading effect app-wide from this single file:

- **To change the speed:** Find the Animated.timing blocks and adjust
  the duration: 1000 value (in milliseconds). A lower number makes it
  pulse faster, and a higher number makes it slower.

- **To change the contrast:** Adjust the outputRange: \[0.3, 0.7\] in
  the opacity interpolation to something wider (like \[0.1, 0.9\]) for a
  more dramatic fade.

- **To change the color:** Find the const baseColor =
  theme.colors.border; line and replace it with a different theme color
  or a specific hex code.

# Problem 24

**//Trending in Feed content not appearing problem:**

This has been a classic React Native debugging journey---moving from a
visual \"red block\" test to a deep-dive into API data structures. Here
is the summary of how we diagnosed and resolved the **Trending in Feed**
issue.

## **🛠 The Debugging Process: Step-by-Step**

1.  **The Visual Test (The Red Block):** We started by adding a fixed
    height and a red background to TrendingFeed.tsx. This confirmed the
    component *existed* in the layout but was rendering with zero
    height, hiding its internal content.

2.  **The Orchestrator Audit:** We reviewed Home.tsx and confirmed it
    uses a FlatList to manage sections. This was the first major
    \"aha!\" moment regarding layout.

3.  **The API Deep Dive:** We examined useDiscussion.ts and
    discussion.service.ts to see how the data was being fetched and if
    the \"plumbing\" between the server and the UI was connected.

4.  **The Log Inspection:** You added console.log statements to
    TrendingFeed.tsx. The logs revealed two things: the data path was
    deeper than expected (data.data.items) and the items array was
    currently empty on the server.

5.  **The Final Refactor:** We converted the inner FlatList to a .map()
    to fix the layout and added logic to hide the section entirely if no
    trending data exists.

## **📂 Related Files & Key Culprits**

The problem was spread across three main areas:

+--------------------------------------------+--------------+-----------------------------------+
| **File Path**                              | **Role**     | **The \"Culprit\" Code / Issue**  |
+--------------------------------------------+--------------+-----------------------------------+
| **src/screens/home/Home.tsx**              | The          | Used a FlatList as the main       |
|                                            | Orchestrator | container, which conflicted with  |
|                                            |              | the child FlatList.               |
+--------------------------------------------+--------------+-----------------------------------+
| **src/components/home/TrendingFeed.tsx**   | The UI       | **Culprit 1:** Nested a FlatList  |
|                                            | Component    | inside the parent\'s FlatList,    |
|                                            |              | causing a height of 0.            |
|                                            |              |                                   |
|                                            |              | **Culprit 2:** pathOr(\[\],       |
|                                            |              | \[\'items\'\], data) was missing  |
|                                            |              | the first data layer.             |
+--------------------------------------------+--------------+-----------------------------------+
| **src/api/services/discussion.service.ts** | The Data     | Used Axios, which wraps the       |
|                                            | Service      | server response in an extra .data |
|                                            |              | object.                           |
+--------------------------------------------+--------------+-----------------------------------+
| **src/i18n/locales/en.json**               | Localization | Had multiple similar keys         |
|                                            |              | (trendinginfeed vs trendingFeed), |
|                                            |              | causing potential naming          |
|                                            |              | confusion.                        |
+============================================+==============+===================================+

## **🚫 The Two Key Culprits**

### **1. The \"VirtualizedList\" Conflict**

**Code:** FlatList (Home) \> FlatList (TrendingFeed)

**Problem:** You cannot nest a vertical FlatList inside another vertical
FlatList without a fixed height. The inner list collapses and becomes
invisible. This also triggered the console warning: *\"VirtualizedLists
should never be nested\...\"*.

### **2. The Data Path Mismatch**

**Code:** const mockFeedData = pathOr(\[\], \[\'items\'\], data);

**Problem:** Your API log showed the structure was actually data -\>
data -\> items. The component was looking at the wrong level of the
object, so it always thought the list was empty even if the server had
sent data.

## **✅ The Final Solution**

We refactored TrendingFeed.tsx to:

1.  **Use .map()** instead of FlatList to play nice with the Home.tsx
    orchestrator.

2.  **Use the correct path** \[\'data\', \'items\'\] to reach the actual
    list of posts.

3.  **Return null** when the list is empty so the section disappears
    cleanly.

**Now that TrendingFeed is handled, would you like me to help you
refactor RecommendedCommunities.tsx next to fix the remaining console
warning?**

//25:

Recommended Communities (title) and the flatlist horizontal alignment
problem:

//best practice

# **1️⃣ Parent screen controls horizontal spacing**

File: **Explore.tsx**

You added the **single source padding** here.

\<View style={\[styles.container, { flex: 1, paddingHorizontal:
theme.spacing.md }\]}\>

### **What this means**

Everything inside the screen should visually start after this spacing.

Visually:

\| screen edge \| padding(md) \| content starts here

So sections like:

- TrendingTopics

- RecommendedCommunities

- TopDiscussions

all align with this **same start line**.

# **2️⃣ Recommended communities section**

File: **RecommendedCommunities.tsx**

Your section header:

\<SectionHeader

title={\`\${t(\'common.recommended\')} \${t(\'common.communities\')}\`}

/\>

Because Explore.tsx already has padding, the header appears correctly:

\| edge \| padding(md) \| Recommended Communities

So the **header is already aligned correctly**.

# **3️⃣ The FlatList problem**

Inside the same file you render a horizontal list:

\<FlatList

horizontal

renderItem={renderItem}

/\>

FlatList items start **immediately from the container edge**.

Without fixing it, the layout becomes:

\| edge \| Card1 \| Card2 \| Card3

But the header starts here:

\| edge \| padding(md) \| Recommended Communities

So the **cards start too far left** compared to the header.

# **4️⃣ Why we add marginLeft**

Inside **renderItem**:

const renderItem = ({ item: community, index }) =\> (

\<TouchableOpacity

style={\[

styles.cardContainer,

index === 0 && { marginLeft: theme.spacing.md }

\]}

\>

We add margin **only to the first card**.

Result:

\| edge \| padding(md) \| Card1 \| Card2 \| Card3

Now cards align with the header.

# **5️⃣ Why use theme.spacing.md**

Because your **screen padding uses md**.

File: **Explore.tsx**

paddingHorizontal: theme.spacing.md

So we match the same spacing:

marginLeft: theme.spacing.md

If you used a different value like:

marginLeft: theme.spacing.sm

Then alignment breaks:

\| edge \| padding(md) \| header

\| edge \| padding(sm) \| Card1

Everything would look slightly shifted.

Using **the same spacing token keeps the design system consistent**.

# **6️⃣ Why only for the first card**

Your card style already has spacing **between cards**.

File: **RecommendedCommunities.tsx**

cardContainer: {

marginRight: theme.spacing.sm,

}

So layout becomes:

\| padding \| Card1 \| gap \| Card2 \| gap \| Card3

If we added marginLeft to **all cards**, you\'d get double spacing.

So we check:

index === 0

Meaning:

only the first card gets marginLeft

# **Final layout (correct)**

Explore.tsx

paddingHorizontal: md

│

├ SectionHeader (Recommended Communities)

│

└ FlatList

marginLeft(md) → first card

│

├ Card1

├ Card2

└ Card3

Everything starts from the **same visual line**.

✅ So the rule you applied is:

**Parent controls layout → FlatList first item respects that layout.**

# Problem 26

Here's a **clean summary of the issue and the best practice you
applied**.

## **Problem**

Initially, the modal system stored **UI (JSX) inside state**, something
like:

setDialogConfig({

title: \'\',

content: \<SomeComponent /\>

});

This causes several issues in React:

- **JSX becomes frozen in state**

- **Props can become stale**

- **Closures may capture old values**

- React **may not re-render correctly**

- Leads to bugs like **theme selection not updating or modal content not
  reacting to state changes**

In short, **React state should not store UI elements**.

## **Best Practice**

Instead of storing JSX, store **only the modal type** (UI state).

Example:

const \[activeModal, setActiveModal\] = useState\<

\'theme\' \| \'language\' \| \'logout\' \| null

\>(null);

Then render UI based on that state:

\<CommonDialog

visible={activeModal !== null}

onDismiss={hideDialog}

content={

activeModal === \'theme\' ? \<ThemeSelectionDialogContent /\> :

activeModal === \'language\' ? \<LanguageSelection /\> :

activeModal === \'logout\' ? \<LogoutConfirmation /\> :

null

}

/\>

## **Why This Is Better**

  ---------------------------------------
  **Old Pattern**    **Best Practice**
  ------------------ --------------------
  JSX stored in      Only modal type
  state              stored

  Props can become   Always fresh props
  stale              

  Hard to debug      Predictable behavior

  Can cause UI bugs  React re-renders
                     correctly
  ---------------------------------------

## **Key React Rule**

**Never store UI in state.**

Avoid storing:

- JSX elements

- React components

- hooks

- closures containing props/state

Store only **serializable UI state**, such as:

modal: \"logout\"

activeTab: \"settings\"

selectedUserId: 42

## **Result**

By switching to:

const \[activeModal, setActiveModal\] = useState\<\'theme\' \|
\'language\' \| \'logout\' \| null\>(null);

your modal system becomes:

- predictable

- reactive

- easier to maintain

- aligned with React best practices.

//BEST PRACTICE:

# **Best Practice: Move React Native Styles Outside Components Using a Style Factory**

### **Problem**

In React Native, defining styles with StyleSheet.create() **inside a
component** causes the styles to be **recreated on every render**.

Example of the anti-pattern:

const MyComponent = () =\> {

const styles = StyleSheet.create({

container: {

backgroundColor: theme.colors.background,

},

});

return \<View style={styles.container} /\>;

};

Every render will create a **new style object**, which is unnecessary
and can impact performance in larger components.

### **Best Practice**

Move the styles **outside the component** and create a **style factory
function** that receives dependencies such as the theme.

Example:

const MyComponent = () =\> {

const theme = useTheme();

const styles = createStyles(theme);

return \<View style={styles.container} /\>;

};

const createStyles = (theme: AppTheme) =\>

StyleSheet.create({

container: {

backgroundColor: theme.colors.background,

},

});

### **Benefits**

1.  **Avoids recreating style objects on every render**

2.  **Improves performance for large components**

3.  **Keeps components cleaner and easier to read**

4.  **Encourages separation of UI logic and styling**

5.  **Makes styles reusable and easier to maintain**

### **Where to Apply This**

This pattern is especially useful when:

- Components **rerender frequently**

- Styles depend on **theme or props**

- The component contains **large style objects**

- The screen contains **multiple nested components**

### **Example Applied in Our Code**

We refactored styles in:

- SettingsScreen

- SettingItem

- ThemeOptionCard

Each component now uses:

const styles = createStyles(theme);

with the style factory defined **outside the component**.

### **Key Takeaway**

❌ Avoid:

StyleSheet.create() inside components

✅ Prefer:

StyleSheet.create() inside a style factory outside the component

This keeps React Native components **cleaner, faster, and more
maintainable**.

# Problem 26

Here is a **clean summary of the problem and the fix** you implemented.

# **🐞 Problem**

The **category chips under \"Other Events\" were not filtering events**.

When clicking a chip:

- The UI showed a brief loading indicator.

- The API refetched.

- But the **same events were returned every time**, so the list never
  changed.

Logs confirmed this:

Other events: (3) \[{...}, {...}, {...}\]

Even after selecting different categories.

# **🔍 Root Cause**

The frontend was sending the **wrong query parameter** to the backend.

Originally the query was:

useGetEvents({

limit: 3,

\...(selectedCategory ? { category: selectedCategory } : {}),

});

Which generated API requests like:

GET /events?limit=3&category=8

However, the backend API expected the parameter:

categoryId

Since the backend didn\'t recognize category, it **ignored the filter
and always returned the same events**.

# **✅ Solution**

Update the query parameter to match the backend API.

Correct implementation:

const params = {

limit: 3,

\...(selectedCategory && { categoryId: selectedCategory }),

};

const {

data: otherEventsData,

isLoading: isLoadingOther,

isRefetching: isRefetchingOther,

refetch: refetchOther,

} = useGetEvents(params);

Now the API request becomes:

GET /events?limit=3&categoryId=8

The backend correctly filters events by category, and the UI updates
accordingly.

# **🎯 Result**

After the fix:

- Category chips trigger API refetch

- Events are filtered correctly

- UI updates with category-specific events

- No unnecessary query parameters like categoryId=null are sent

# **💡 Additional Best Practice Used**

This pattern ensures clean requests:

\...(selectedCategory && { categoryId: selectedCategory })

It prevents sending:

categoryId=null

when no category is selected.

✅ **Final Outcome:\**
The category filter now works correctly, and events update dynamically
based on the selected chip.

# Problem 27

Here is a clear and concise explanation you can use for your
documentation, code comments, or pull request description to justify the
approach:

### **Why this approach was used in NotificationScreen.tsx**

In **NotificationScreen.tsx**, the text inside the section headers
(specifically \'Earlier\', \'Yesterday\', and \'Received\') was not
aligning correctly with the rest of the list content.

Because the SectionHeader component is shared across multiple screens in
the project, modifying its internal padding directly carried a high risk
of breaking layouts on other pages. To safely fix the alignment for this
specific screen without causing unintended global side effects, the
SectionHeader was wrapped in a local \<View\> to apply the necessary
horizontal padding.

**Code Snippet:**

TypeScript

\<View style={{ paddingHorizontal: theme.spacing.md }}\>

\<SectionHeader title=\"Earlier\" theme={theme} /\>

\</View\>

# Problem 28

Here is a **clean summarized report** of the issue and fix.

# **Problem**

The **category chips shown in the \"Other Events\" section** were **not
appearing in the filter modal** inside the **All Events screen**.

Reason:\
The filter modal (EventFiltersModal.tsx) was using **hardcoded filter
options** instead of the **categories fetched from the API**.

So the UI showed:

Sports

Music

Networking

Tech

Education

instead of the real event categories like:

Anime & Cosplay

Artificial Intelligence

eCommerce

Fintech

# **Root Cause**

Categories were fetched in:

Events.tsx

but **not passed down to the filter modal**.

Component hierarchy:

Events.tsx

↓

EventListBottomSheet.tsx

↓

EventList.tsx

↓

EventFiltersModal.tsx

The modal had **no access to API categories**.

# **Files Modified**

Events.tsx

EventListBottomSheet.tsx

EventList.tsx

EventFiltersModal.tsx

# **Original Problem Code**

### **File**

EventFiltersModal.tsx

Hardcoded filters:

const EVENT_FILTERS = \[

{ id: \'sports\', label: \'Sports\' },

{ id: \'music\', label: \'Music\' },

{ id: \'networking\', label: \'Networking\' },

{ id: \'tech\', label: \'Tech\' },

{ id: \'education\', label: \'Education\' },

\];

Used in UI:

{EVENT_FILTERS.map(option =\> {

const isSelected = localFilter === option.id;

return (

\<TouchableOpacity

key={option.id}

onPress={() =\> handleSelect(option.id)}

\>

\<Text\>{option.label}\</Text\>

\</TouchableOpacity\>

);

})}

This ignored the **API categories completely**.

# **Solution**

Pass categories fetched in Events.tsx through the component hierarchy
and use them in the modal.

## **1️⃣ Fetch Categories**

### **File**

Events.tsx

const EVENT_CATEGORIES = pathOr(\[\], \[\'data\', \'categories\'\],
eventCategoriesData);

## **2️⃣ Pass to BottomSheet**

### **File**

Events.tsx

\<EventListBottomSheet

visible={eventListBottomSheetVisible}

onClose={() =\> setEventListBottomSheetVisible(false)}

type={selectedEventType}

categories={EVENT_CATEGORIES}

/\>

## **3️⃣ Pass to EventList**

### **File**

EventListBottomSheet.tsx

\<EventList

type={type}

onClose={onClose}

categories={categories}

/\>

## **4️⃣ Pass to Modal**

### **File**

EventList.tsx

\<EventFiltersModal

visible={isFilterModalVisible}

onClose={() =\> setIsFilterModalVisible(false)}

selectedFilter={selectedFilter}

onApply={setSelectedFilter}

onReset={() =\> setSelectedFilter(null)}

categories={categories}

/\>

## **5️⃣ Render Categories**

### **File**

EventFiltersModal.tsx

Replace hardcoded filters with:

\<View style={styles.chipContainer}\>

{categories.map(category =\> {

const isSelected = localFilter === category.id;

return (

\<TouchableOpacity

key={category.id}

style={\[styles.chip, isSelected && styles.chipSelected\]}

onPress={() =\> handleSelect(category.id)}

\>

\<Text style={\[styles.chipText, isSelected &&
styles.chipTextSelected\]}\>

{category.name}

\</Text\>

\</TouchableOpacity\>

);

})}

\</View\>

# **Final Result**

The **filter modal now shows the same categories as the Events screen**.

Anime & Cosplay

Artificial Intelligence

eCommerce

Fintech

\...

Filtering now works correctly because the modal uses the **same API data
source**.

//best practice:\
Here is a complete summary of the refactoring we just completed,
including the files we touched and the code we changed.

### **What We Did & The Purpose**

We refactored your React Native codebase to centralize your TypeScript
definitions. Before this, you had the Event interface duplicated across
multiple files, and some components were relying on a locally exported
EventCategory from Events.tsx.

**The purpose of creating src/types/event.types.ts was to:**

1.  **Keep your code DRY (Don\'t Repeat Yourself):** By defining the
    types in one place, you only have to update them once if your API or
    data structure changes.

2.  **Improve Accuracy:** We added missing optional fields (bannerUrl,
    backgroundColor, state, stats) to the new interfaces so they
    perfectly match the data your components are already extracting
    using Ramda\'s pathOr.

3.  **Clean Up Component Files:** Removing massive inline interfaces
    from your .tsx files makes the UI code much easier to read and
    maintain.

### **1. The New Type File**

**File:** src/types/event.types.ts

**Action:** Created this file to act as the single source of truth for
all event-related data structures.

TypeScript

/\*\*

\* Event module types

\*/

export interface EventCategory {

id: string;

name: string;

}

export interface EventLocation {

id: string;

city: string;

state?: string;

country: string;

addressLine?: string;

}

export interface EventStats {

going?: number;

registered?: number;

interested?: number;

}

export interface Event {

id: string;

title: string;

description?: string;

startAt?: Date;

eventTime?: Date;

location?: EventLocation;

imageUrl?: string;

bannerUrl?: string;

backgroundColor?: string;

stats?: EventStats;

category?: EventCategory;

attendeesCount?: number;

isUpcoming?: boolean;

}

### **2. Updating the Component Files**

We went through four component files to strip out the old definitions
and wire up the new imports.

#### **File: EventList.tsx**

**Action:** Deleted the 18-line inline Event interface and updated the
import.

- **Added:** import { Event, EventCategory } from
  \'@/types/event.types\';

- **Removed:** import { EventCategory } from \'./Events\';

- **Deleted:**

- TypeScript

interface Event {

id: string;

title: string;

// \... (rest of the old inline interface)

isUpcoming?: boolean;

}

- 
- 

#### **File: Events.tsx**

**Action:** Deleted the duplicate inline Event interface and imported
the new one.

- **Added:** import { Event, EventCategory } from
  \'@/types/event.types\';

- **Deleted:**

- TypeScript

interface Event {

id: string;

title: string;

// \... (rest of the old inline interface)

isUpcoming?: boolean;

}

- 
- 

#### **File: EventFiltersModal.tsx**

**Action:** Updated the import path so it pulls EventCategory from the
new types file instead of Events.tsx.

- **Added:** import { EventCategory } from \'@/types/event.types\';

- **Removed:** import { EventCategory } from \'./Events\';

#### **File: EventListBottomSheet.tsx**

**Action:** Updated the import path to pull EventCategory from the new
types file.

- **Added:** import { EventCategory } from \'@/types/event.types\';

- **Removed:** import { EventCategory } from \'./Events\';

# Problem 29

Here is a **clear professional summary** of the issue and the fix you
implemented. This is the type of explanation you could even include in a
**PR description or debugging note**.

# **Problem Summary**

There was an **inconsistency in event filtering between two screens** in
the React Native app:

1.  **Events Screen**

2.  **All Events Screen (EventList inside BottomSheet)**

Both screens allow users to filter events by **category chips**.

### **Observed Behavior**

  ----------------------------------------------
  **Screen**     **Result**
  -------------- -------------------------------
  Events Screen  Filtering works correctly

  All Events     Filtering does **not** return
  Screen         the same events
  ----------------------------------------------

For example:

Anime & Cosplay selected

- **Events Screen** → shows correct cards

- **All Events Screen** → shows different / unfiltered cards

# **Root Cause**

The two screens were sending **different parameter names to the API**.

### **Working implementation**

File:

src/screens/events/Events.tsx

Code:

const params = {

limit: 3,

\...(selectedCategory && { categoryId: selectedCategory }),

};

const { data: otherEventsData } = useGetEvents(params);

API request:

GET /events?categoryId=8

### **Broken implementation**

File:

src/screens/events/EventList.tsx

Code before fix:

const queryParams = {

scope: \'all\',

eventType,

limit: ITEMS_PER_PAGE,

search: debouncedSearchQuery,

category: selectedFilter,

};

API request:

GET /events?category=8

The backend **expects categoryId**, not category.

Because of this mismatch:

category → ignored by backend

The API returned **unfiltered results**.

# **Data Flow Comparison**

### **Events Screen (Correct)**

Chip press

↓

selectedCategory

↓

useGetEvents()

↓

getEvents({ categoryId })

↓

Filtered events returned

### **All Events Screen (Before Fix)**

Filter modal

↓

selectedFilter

↓

useEventsInfiniteQuery()

↓

getEvents({ category })

↓

Backend ignores filter

↓

Unfiltered events returned

# **Solution**

Standardize the parameter name across both screens.

The **correct parameter is categoryId**.

# **Code Fix**

### **File Modified**

src/screens/events/EventList.tsx

### **Before (Incorrect)**

const queryParams = useMemo(() =\> {

return {

scope: \'all\',

eventType,

limit: ITEMS_PER_PAGE,

search: debouncedSearchQuery,

category: selectedFilter,

};

}, \[eventType, debouncedSearchQuery, selectedFilter\]);

### **After (Correct)**

const queryParams = useMemo(() =\> {

return {

scope: \'all\',

eventType,

limit: ITEMS_PER_PAGE,

search: debouncedSearchQuery,

\...(selectedFilter && { categoryId: selectedFilter }),

};

}, \[eventType, debouncedSearchQuery, selectedFilter\]);

# **Why this fix works**

Now both screens send the **same API parameter**.

### **Events Screen**

GET /events?categoryId=8

### **All Events Screen**

GET /events?categoryId=8

Since the backend expects categoryId, the filter works correctly on both
screens.

# **Verification via Debug Logs**

Logs confirmed the correct data flow.

### **Before fix**

API getEvents params: { category: 8 }

### **After fix**

API getEvents params: { categoryId: 8 }

And the request pipeline became:

Filter UI

↓

selectedFilter

↓

queryParams

↓

useEventsInfiniteQuery

↓

getEvents()

↓

GET /events?categoryId=8

# **Files Involved**

### **UI Components**

src/screens/events/Events.tsx

src/screens/events/EventList.tsx

src/screens/events/EventFiltersModal.tsx

src/screens/events/EventListBottomSheet.tsx

### **React Query Hooks**

src/api/hooks/useEvents.ts

### **API Services**

src/api/services/event.service.ts

# **Final Result**

After fixing the parameter name:

  ------------------------------------
  **Feature**        **Status**
  ------------------ -----------------
  Events screen      ✅ Works
  filter             

  All events screen  ✅ Works
  filter             

  API request        ✅ Correct
                     parameter

  Backend filtering  ✅ Applied
  ------------------------------------

The filtering behavior is now **consistent across both screens**.

# Problem 30

### **🛠️ Debugging Summary: Unclickable Full Name Field**

**1. The Problem**

The \"Full Name\" input field in the PersonalDataStep form was
non-interactive. Users could see the field but were unable to tap it or
type a custom name, despite the expectation that this field should be
editable.

**2. Root Cause Analysis**

The configuration for the FormInput component explicitly included a
disabled: true property. In React Native, this property translates to
editable={false} or pointerEvents=\"none\", which completely blocks user
interaction and keyboard activation.

**3. Code Files & Fixes**

#### **File: src/screens/PersonalDataStep.tsx**

**Before (Buggy Code):**

The disabled prop was hardcoded to true, locking the input.

TypeScript

\<FormInput

config={{

type: \'text\',

control,

name: \'fullName\',

placeholder: \'Full Name\',

label: \'Full Name\',

variant: \'labeled\',

disabled: true, // ❌ This is blocking user input

keyboardType: \'default\',

error: errors.fullName,

rules: { required: \'Full Name is required\' },

}}

/\>

**After (Corrected Code):**

Setting disabled to false (or removing it) restores interactivity.

TypeScript

\<FormInput

config={{

type: \'text\',

control,

name: \'fullName\',

placeholder: \'Full Name\',

label: \'Full Name\',

variant: \'labeled\',

disabled: false, // ✅ Field is now clickable and editable

keyboardType: \'default\',

error: errors.fullName,

rules: { required: \'Full Name is required\' },

}}

/\>

**4. Final Verification**

- **Interaction:** Tapping the field now triggers the system keyboard.

- **Data Flow:** Changes typed by the user will now correctly update the
  fullName value in react-hook-form state via the control object.

- **Consistency:** Note that the **Email** field in your file is also
  set to disabled: true. If you want users to be able to edit their
  email as well, you should apply the same fix there.

# Problem 31

### **🛠️ Debugging Summary: Company Profile Image Upload Failure**

#### **1. The Problem**

The company profile image failed to update or persist. While the UI
interaction occurred, the backend returned a **400 Bad Request** stating
\"No avatar file provided\". Even after the error was resolved, the UI
would not visually update with the new image, making it appear as if the
upload had failed.

#### **2. Root Cause Analysis**

- **Key Mismatch:** The backend expected the multipart/form-data key
  avatar, but the generic useMediaPickerUpload hook was hardcoded to
  send files under the key document.

- **Endpoint Misdirection:** The generic hook automatically triggered a
  mutation for uploadDocument (general storage) instead of the specific
  uploadCompanyAvatar endpoint required for profile processing.

- **Import Error:** A specific mutation (useUploadCompanyAvatar) was
  missing a crucial import for the service function, causing a silent
  crash in the logic.

- **Image Caching:** React Native\'s \<Image /\> component cached the
  old URI. Since the URL string remained identical after the refresh,
  the UI did not re-fetch the new pixel data.

#### **3. Code Files & Fixes**

**File:** src/hooks/useMediaPickerUpload.ts

**Fix:** Decoupled picking from uploading by exporting a standalone
pickMedia function.

TypeScript

// Added pickMedia to the hook return

export const useMediaPickerUpload = (fileKey: string = \'document\') =\>
{

const pickMedia = React.useCallback(async (mediaType: MediaType) =\> {

const res = await pick({

type: mediaType === \'image\' ? \[types.images\] : \[types.pdf\],

copyTo: \'cachesDirectory\',

});

return Array.isArray(res) ? res\[0\] : res;

}, \[\]);

return { pickMedia, pickAndUpload, \... };

};

**File:** src/api/hooks/useUpload.ts

**Fix:** Corrected the mutation to use the proper service and handle the
companyId payload.

TypeScript

import { uploadCompanyAvatar } from \'../services/upload.service\'; //
✅ Fixed missing import

export const useUploadCompanyAvatar = () =\> {

return useMutation({

mutationFn: ({ payload, companyId }) =\> uploadCompanyAvatar(payload,
companyId),

});

};

**File:** src/components/CompanyProfileCard.tsx

**Fix:** Manually constructed FormData with the avatar key and added a
**Cache Buster** to the image source.

TypeScript

// Inside handleEditUpdateAvatar

const formData = new FormData();

formData.append(\'avatar\', {

uri: file.uri,

name: \`avatar-\${Date.now()}.jpg\`,

type: \'image/jpeg\',

} as any);

// Inside the return statement

\<CompanyAvatar

source={{

uri: companyData?.logoUrl

? \`\${companyData.logoUrl}?t=\${new Date().getTime()}\` // ✅ Forces UI
refresh

: \'\'

}}

/\>

#### **4. Final Verification**

- **Network Request:** Logs confirm a POST to
  /upload/update_company_avatar/121 with a **201 Created** status.

- **Data Integrity:** The backend response now returns a valid fileUrl
  from Azure Blob Storage.

- **UI Sync:** The \"Cache Buster\" ensures that the new image appears
  immediately after the refresh() call without requiring a manual app
  restart.

**Would you like me to help you apply this \"Cache Buster\" logic to
other profile sections like the User\'s personal avatar?**

# Problem 32

**FIXED COMPANY AVATAR PROFILE ICON AND the camera icon inside it, also
added preview mode.**

In this session, we refined the **CompanyAvatar** component to improve
its layout, fixed a clipping issue with the camera icon, and implemented
a standard full-screen preview mode.

Here is the summary of the changes:

## **1. File: companyProfileStyles.ts**

**Goal:** Fix the layout issue where the profile section was touching
the top of the screen.

- **Action:** Added marginTop to the main profile container to provide
  breathing room from the header.

- **Snippet:**

- TypeScript

profileCardContainer: {

alignItems: \'center\',

justifyContent: \'center\',

marginTop: theme.spacing.xl, // Pushes the profile down

},

- 
- 

## **2. File: CompanyAvatar.tsx (Styling)**

**Goal:** Prevent the camera icon from touching the outer container\'s
invisible boundary.

- **Action:** Changed the absolute positioning from negative values
  (which pushed the icon outside the avatar) to positive values (which
  nested it cleanly inside the corner).

- **Snippet:**

- TypeScript

icon: {

position: \'absolute\',

bottom: 4, // Inward from bottom

right: 4, // Inward from right

},

- 
- 

## **3. File: CompanyAvatar.tsx (Preview Mode)**

**Goal:** Allow users to tap the image to see a full-screen version,
following industry standards.

- **Implementation:** \* Added a Modal component to handle the overlay.

  - Used useState (isPreviewVisible) to toggle the view.

  - Wrapped the existing avatar in a TouchableHighlight that triggers
    the modal.

- **Permissions Logic:** We removed the disabled prop from the main
  container. Now, **all users** can tap to preview, but only **owners**
  see the IconButton (camera) required to edit the image.

- **Full Implementation Snippet:**

- TypeScript

// The main wrapper now triggers the preview

\<TouchableHighlight onPress={() =\> setPreviewVisible(true)}\>

\<View style={\...}\>

\<Image source={avatarSource} style={styles.avatar} /\>

{showEdit && \<IconButton \... /\>} {/\* Only owners see this \*/}

\</View\>

\</TouchableHighlight\>

{/\* The Modal that appears on top \*/}

\<Modal visible={isPreviewVisible} transparent={true}
animationType=\"fade\"\>

\<TouchableOpacity style={styles.modalContainer} onPress={() =\>
setPreviewVisible(false)}\>

\<Image source={avatarSource} style={styles.fullImage}
resizeMode=\"contain\" /\>

\</TouchableOpacity\>

\</Modal\>

- 
- 

### **Key Takeaway**

The final component now distinguishes between **\"Viewing\"** (Global
access via the main image) and **\"Editing\"** (Owner-only access via
the camera icon), while ensuring the UI is polished and doesn\'t overlap
awkwardly.

**Would you like me to help you add a \"Download Image\" button inside
the preview modal so users can save the company logo?**

# Problem 33

Here is a complete summary of the debugging session for your future
reference. You successfully tracked down and patched a widespread React
Native list-rendering bug.

## **🚨 The Problem: Duplicate Keys**

You were encountering the React \"Red Screen of Death\" with variations
of this error message:

> Encountered two children with the same key, %s. Keys should be unique
> so that components maintain their identity across updates. Non-unique
> keys may cause children to be duplicated and/or omitted --- the
> behavior is unsupported and could change in a future version. .\$1551
>
> *(Later changed to .\$1552 as we fixed the first instance).*

### **What the Error Means**

In React, whenever you render a list of elements (using .map() or a
FlatList), every item must have a 100% unique key prop.

- The .\$ prefix in the error indicates that React was receiving a **raw
  value** (like an integer 1551 or 1552) directly from your database ID,
  without any string prefix.

- Because your API/state was sometimes returning duplicate items (e.g.,
  the \"Rapper\" post showing up twice in your Feed), React found two
  items with the exact same raw ID and crashed.

## **🛠️ The Files & Code Fixes**

We tracked down the raw item.id usage across several files and
implemented the **\"Composite Key Pattern\"** (Prefix + ID + Index) to
guarantee uniqueness.

### **1. CommentCard.tsx (The .\$1551 Fix)**

**The Issue:** Nested replies were mapping over comment.replies using
only the raw reply.id. If a reply had a colliding ID, it crashed.

**The Fix:** Added index to the .map() function and created a highly
specific string key.

TypeScript

// ❌ BEFORE

{comment.replies.map((reply: any) =\> (

\<CommentCard key={reply.id} \... /\>

))}

// ✅ AFTER

{comment.replies.map((reply: any, index: number) =\> (

\<CommentCard

key={\`comment-\${comment.id}-reply-\${reply.id \|\| index}-\${index}\`}

\...

/\>

))}

### **2. NotificationBanners.tsx**

**The Issue:** A hardcoded array of notifications was being mapped using
raw integer IDs (1, 2, 3).

**The Fix:** Appended a prefix and the index.

TypeScript

// ❌ BEFORE

{notifications.map(item =\> (

\<NotificationBannerItem key={item.id} \... /\>

))}

// ✅ AFTER

{notifications.map((item, index) =\> (

\<NotificationBannerItem

key={\`notification-banner-\${item.id}-\${index}\`}

\...

/\>

))}

### **3. QForU.tsx (The .\$1552 Fix)**

**The Issue:** When rendering different sections (\"Posts Shared\" and
\"Liked Posts\"), the parent component was passing the raw item.id to
the child \<PostCard\>. If a user liked and shared the same post, the ID
appeared twice on the same screen.

**The Fix:** Added section-specific prefixes to the keys.

TypeScript

// ❌ BEFORE (In both \"Posts Shared\" and \"Liked Posts\" sections)

renderSection(\'Posts Shared\', postsShared, item =\> (

\<PostCard key={item.id} \... /\>

))

// ✅ AFTER

renderSection(\'Posts Shared\', postsShared, item =\> (

\<PostCard key={\`posts-shared-\${item.id}\`} \... /\>

))

// And for Liked Posts:

\<PostCard key={\`liked-posts-\${item.id}\`} \... /\>

### **4. Feed.tsx (The Root UI Crash)**

**The Issue:** Your FlatList was using a keyExtractor that only returned
the raw ID. Because your API fetched the exact same \"Snoop doggy\" post
twice, the FlatList crashed.

**The Fix:** Updated the keyExtractor to utilize both the item.id and
the index.

TypeScript

// ❌ BEFORE

const keyExtractor = React.useCallback((item: Post) =\> item.id, \[\]);

// ✅ AFTER

const keyExtractor = React.useCallback(

(item: Post, index: number) =\> \`user-feed-\${item.id}-\${index}\`,

\[\]

);

## **🛡️ How to Avoid This in the Future**

To prevent this from happening as your app scales, follow these three
rules:

1.  **Never use key={item.id} by itself:** Database IDs are great, but
    they aren\'t safe from frontend state collisions or backend
    pagination glitches. Always combine them into a string.

2.  **Use the \"Belt and Suspenders\" Pattern:** The safest formula for
    a React key inside a list is:\
    key={\`ComponentOrScreenName-\${item.id}-\${index}\`}\
    This ensures that even if the backend completely fails and sends you
    10 identical items, the frontend UI will still render smoothly
    because the index will always be unique.

3.  **Audit your keyExtractors:** Whenever you create a new FlatList or
    ScrollView, immediately write the keyExtractor with a string prefix
    and index, rather than relying on React Native\'s default behavior.

### **⚠️ The Underlying Backend Issue**

Keep in mind: **The frontend fixes above are band-aids.** They stop the
app from crashing, but they do not fix the fact that your useUserFeed
API call is returning duplicate data (like the duplicate \"Rapper\"
posts). You will eventually need to debug your backend pagination logic
or your frontend state-merging logic (e.g., making sure that when you
\"pull to refresh,\" you don\'t accidentally append the same posts to
the existing feed array).

Would you like to look at the useUserFeed hook next to figure out why
the API is serving duplicates, or is there another feature you want to
work on?

Here is the master list of every file that was updated and fixed during
this entire debugging process to resolve the duplicate key errors. Keep
this handy as a reference for your \"Composite Key Pattern\" (prefix +
id + index).

### **🛠️ Phase 1: Your Initial Audit & Fixes**

These are the files you successfully refactored before we tackled the
final stubborn errors:

- **CreatePost.tsx**: Hardcoded unique keys for attachments.

- **HashtagSelector.tsx**: Added index fallbacks to the tag pills.

- **HashtagSelectModal.tsx**: Added index fallbacks to the suggested
  tags list.

- **CommunitySelectModal.tsx**: Added index fallbacks to the community
  list.

- **TrendingFeed.tsx**: Switched list rendering to use
  key={\`trending-\${item.id}-\${index}\`}.

- **JobPostings.tsx**: Cleaned up the keyExtractor and removed
  Math.random().

- **ActivityViewAll.tsx**: Updated the keyExtractor and removed manual
  key={key} props.

### **🕵️‍♂️ Phase 2: The Deep Dive (Collaborative Fixes)**

These are the hidden or nested files we tracked down together to
eliminate the .\$1551 and .\$1552 crashes:

- **CommentCard.tsx**:

  - *The Fix:* Fixed the recursive nested replies by adding the index
    argument to the .map() function.

  - *The Pattern:* key={\`comment-\${comment.id}-reply-\${reply.id \|\|
    index}-\${index}\`}

- **PostCard.tsx**:

  - *The Fix:* Added defensive keying to the media/image container to
    prevent future collisions if image IDs overlap with post IDs.

  - *The Pattern:* key={\`post-image-\${post.id}-\${pathOr(\'0\',
    \[\'media\', \'0\', \'id\'\], post)}\`}

- **NotificationBanners.tsx**:

  - *The Fix:* Updated the hardcoded notifications list mapping to
    prevent raw integer collisions (1, 2, 3).

  - *The Pattern:* key={\`notification-banner-\${item.id}-\${index}\`}

- **QForU.tsx**:

  - *The Fix:* Updated the parent-level wrapper keys (qforu-section-),
    but more importantly, fixed the raw item.id being passed directly to
    the \<PostCard /\> components inside the \"Posts Shared\" and
    \"Liked Posts\" sections.

  - *The Pattern:* key={\`posts-shared-\${item.id}\`} and
    key={\`liked-posts-\${item.id}\`}

- **Feed.tsx**:

  - *The Fix:* The root cause of the UI crash. The API was serving
    duplicate posts, and the FlatList couldn\'t handle it. We updated
    the keyExtractor.

  - *The Pattern:* keyExtractor={(item, index) =\>
    \`user-feed-\${item.id}-\${index}\`}

**Pro-Tip for your next session:** Whenever you copy/paste code to
create your other feed tabs (like Explore or Activities), make sure to
check their keyExtractor functions so you don\'t accidentally copy the
old bug over!

Would you like me to help you look into the useUserFeed API hook next to
see why it\'s returning duplicate data in the first place?

# Problem 34

Here is a summary of the task and the final solution we implemented:

### **The Task**

The goal was to implement a custom toast notification for the company
avatar upload flow that perfectly matched your Figma design.

**Key design requirements:**

- **Shape & Placement:** A fully rounded pill-shaped container
  positioned at the bottom center of the screen.

- **Icon Structure:** A layered dual-circle design featuring a soft,
  semi-transparent outer \"halo\" and a solid inner circle containing a
  white checkmark (✓) or exclamation mark (!).

- **Theming:** Strict background colors for the toast container (#1A1A1A
  for dark mode, #FFFFFF for light mode).

- **Scope:** Restricting the design to only success (green) and error
  (red) states, discarding unnecessary warning/info states for this
  specific flow.

### **The Discovery & Solution**

Initially, we looked at useToastConfig.tsx (which belongs to the
react-native-toast-message library). However, after reviewing App.tsx,
we discovered your application\'s architecture actually uses a custom
global provider built on top of **React Native Paper\'s \<Snackbar\>**.

To fix the issue, we bypassed the unused toast library files and applied
the Figma styles directly to your active global Snackbar component.

### **Modified Files**

**1. src/components/toast/SnackbarProvider.tsx (The UI Fix)**

- **Layered Icons:** Replaced the single iconContainer with a nested
  outerCircle (using an alpha transparency of 0.2 for the halo) and
  innerCircle (solid color).

- **White Icons:** Forced the \<Icon /\> component to render with
  color=\"#FFFFFF\".

- **Pill Shape:** Updated makeStyles to give the main container
  borderRadius: 100.

- **Strict Backgrounds:** Added a ternary operator (theme.isDark ?
  \'#1A1A1A\' : \'#FFFFFF\') to the \<Snackbar\> style and theme props
  to override the default surface colors.

**2. CompanyProfileCard.tsx (The Trigger)**

- **Integration:** Imported your custom toast/snackbar hook.

- **Execution:** Added the success(\'Avatar updated successfully\') and
  error(\'Failed to update avatar\') calls directly inside the onSuccess
  and onError callbacks of your handleUploadCompanyAvatarMutate
  function.

Would you like me to help you clean up or remove the unused
react-native-toast-message files from your codebase to keep things tidy?

# Problem 35

Username and userprofile not showing when creating a post in 'New Post'
screen.

It's great to hear everything is finally working! The \"stuck at
loading\" and \"@guest\" issues are classic hurdles in React Native when
dealing with asynchronous storage and external APIs.

Here is a summary for your documentation and future reference.

## **📋 Problem Summary**

The app suffered from three synchronized issues:

1.  **Hydration Race Condition:** The UI was checking for user data
    before AsyncStorage had finished loading it into the Zustand store.

2.  **State Logic Lock:** The updateUser function in the store was
    written to only update if a user *already* existed, preventing the
    initial login data from saving.

3.  **Property Mismatch:** The UI was looking for user.name and
    user.avatar, but the API was providing user.fullName and
    user.avatarUrl.

## **🛠️ The Solution (Before vs. After)**

### **1. src/App.tsx (App-Wide Hydration Guard)**

**Problem:** The Navigator loaded before the store was ready.

- **Before:** Rendered \<AppNavigator /\> immediately.

- **After:** Added a check to block rendering until hydration is
  complete.

TypeScript

// Inside AppContent

if (!isHydrated) return \<\>\</\>;

return \<AppNavigator /\>;

### **2. src/store/authStore.ts (Store Logic)**

**Problem:** updateUser ignored updates if the current state was null.

- **Before:** if (user) { set({ \... }) }

- **After:** Allowed setting the object even if currently null.

TypeScript

updateUser: (updatedUser: Partial\<any\>) =\> {

const { user } = get();

set({ user: user ? { \...user, \...updatedUser } : updatedUser });

},

### **3. src/api/hooks/useAuth.ts (Authentication Hook)**

**Problem:** Login only updated the profile but didn\'t flip the
\"Logged In\" flag.

- **Before:** useAuthStore.getState().updateUser(data.user);

- **After:** Used the login() method to set data and isAuthenticated:
  true.

TypeScript

onSuccess: (data: AuthResponse) =\> {

useAuthStore.getState().login(data.user);

},

### **4. src/screens/CreatePost.tsx (UI Mapping)**

**Problem:** Wrong property keys used for the user object.

- **Before:** user.name and user.avatar

- **After:** Mapped to API-specific keys.

TypeScript

// Text

\@{user?.fullName \|\| \'Guest\'}

// Image

uri: user?.avatarUrl \|\| \'fallback_url\'

## **🛡️ How to prevent this in the future?**

To avoid these \"ghost\" bugs and property mismatches, follow these
three rules:

### **1. Centralize your Hydration**

Never handle isHydrated inside individual screens. Always use the
**Global Hydration Guard** in App.tsx. This ensures that by the time any
screen component code runs, the data is guaranteed to be present.

### **2. Trust but Verify (Logs)**

When integrating a new API endpoint, **always** console.log the raw
response before writing the UI. APIs rarely match your local TypeScript
interfaces perfectly. A 5-second log prevents 2 hours of debugging
\"missing\" data.

### **3. Use Explicit Store Methods**

Avoid using updateUser for primary actions like Login or Logout. Create
explicit methods in your Zustand store (like the login function you
have) that handle all related state changes (tokens, flags, and user
data) in one atomic transaction.

**Is there any other part of the Create Post screen or the User Profile
you\'d like to dynamicize next?**

# Problem 36

For future reference, here is the technical summary of the issue and the
resolution.

## **Problem Summary**

The \"Select Community\" dropdown in the **Create Post** screen was
successfully capturing the user\'s selection, but failed to display the
result (name and image) correctly on the previous screen. There were two
primary causes:

1.  **Data Property Mismatch:** The API returns the image URL in the
    field icon_url, but the component was strictly looking for
    avatar_url.

2.  **Style Conflict:** The CommunityDropdown was reusing styles meant
    for a full-width list item (CommunitySelectModal), causing the
    layout to clip or behave incorrectly when rendered inside a small
    \"pill\" container.

## **Involved Files**

- **CreatePost.tsx**: The parent component using react-hook-form to
  manage the state.

- **CommunityDropdown.tsx**: The UI component responsible for displaying
  the current selection and triggering the selection modal.

- **CommunitySelectModal.tsx**: (Referenced) The source of the shared
  styles that caused layout conflicts.

## **Key Code Snippets**

### **1. The State Linkage (CreatePost.tsx)**

The parent must \"watch\" the form state and pass it down as a prop so
the dropdown can react to changes.

TypeScript

const selectedCommunity = watch(\'community\');

\<CommunityDropdown

handleSelectSelectCommunity={(communityData: any) =\>

setValue(\'community\', communityData)

}

selectedCommunity={selectedCommunity}

/\>

### **2. Resolving the Data Mismatch (CommunityDropdown.tsx)**

The fix involved checking for both avatar_url and icon_url to ensure the
image renders regardless of the API\'s naming convention.

TypeScript

// Inside CommunityDropdown render logic

const displayImage = selectedCommunity.avatar_url \|\|
(selectedCommunity as any).icon_url;

{displayImage ? (

\<Image

source={{ uri: displayImage }}

style={styles.communityAvatar}

/\>

) : (

\<View style={styles.communityAvatarPlaceholder}\>

\<Text\>{initialLetter}\</Text\>

\</View\>

)}

### **3. Layout Fix (Conceptual)**

To prevent the selection from being \"cut off,\" the internal containers
were adjusted to prevent flex: 1 behavior, allowing the pill to
shrink-wrap the text.

TypeScript

// Overriding the shared list styles for the compact pill view

\<View style={\[listItemStyles.communityInfo, { flex: 0, minWidth: 0
}\]}\>

\<Text style={{ fontSize: 12 }} numberOfLines={1}\>

{selectedCommunity.name}

\</Text\>

\</View\>

## **Debugging Checklist for Future Issues**

- **Log the Selection:** Always console.log the object returned from a
  modal/picker to verify property names (e.g., id vs uuid, icon_url vs
  avatar_url).

- **Check Prop Propagation:** Verify the parent is actually passing the
  updated state back down to the child component.

- **Style Overrides:** When reusing styles from a List Item in a Header
  or Pill, explicitly override width, padding, and flex properties.

# Problem 37

STATUS BAR PROBLEM IN LIGHT AND DARK MODE

### **📝 Issue Note: Status Bar & Navigation Bar in Dark Mode**

**The Problem:** When the app was switched to Dark Mode, the top status
bar icons became invisible (black text on a dark background), and a
harsh white strip appeared at the bottom of the screen (the system
navigation bar area).

**The Root Cause:**

1.  **Top Bar:** The system status bar icons were not instructed to
    switch to a light color (light-content) when the dark theme was
    active.

2.  **Bottom Bar:** The outermost container of the app (SafeAreaView)
    lacked an explicit background color. On Android, areas outside the
    standard view (like the space behind the navigation
    gestures/buttons) default to white unless the parent view explicitly
    fills them with a dark color.

### **📂 Files Modified**

#### **1. src/components/CustomStatusBar.tsx**

**What changed:** We removed hardcoded colors, made the background fully
transparent, and passed the barStyle down so the parent could control
the icon colors.

TypeScript

import React from \'react\';

import { StatusBar, type StatusBarStyle } from \'react-native\';

interface CustomStatusBarProps {

barStyle?: StatusBarStyle;

backgroundColor?: string;

translucent?: boolean;

}

const CustomStatusBar: React.FC\<CustomStatusBarProps\> = ({

barStyle = \'dark-content\',

backgroundColor = \'transparent\', // Crucial: lets the parent
container\'s color show through

translucent = true,

}) =\> {

return (

\<StatusBar

barStyle={barStyle}

backgroundColor={backgroundColor}

translucent={translucent}

/\>

);

};

export default CustomStatusBar;

#### **2. App.tsx**

**What changed:** We dynamically calculated the background color based
on the theme and applied it to the SafeAreaView and
GestureHandlerRootView. We also ensured the logic ran *after* the state
was fully loaded.

TypeScript

// Inside AppContent component\...

// 1. Hydration Guard: wait for store to load

if (!isHydrated) {

return \<\>\</\>;

}

// 2. Compute color AFTER hydration

const appBackgroundColor = theme.isDark ? theme.colors.background :
\'#FFFFFF\';

return (

// 3. Apply background color to outermost views to cover top/bottom
system insets

\<GestureHandlerRootView style={\[styles.container, { backgroundColor:
appBackgroundColor }\]}\>

\<SafeAreaProvider\>

\<SafeAreaView

style={\[styles.container, { backgroundColor: appBackgroundColor }\]}

edges={\[\'top\', \'left\', \'right\', \'bottom\'\]}

\>

\<PaperProvider theme={paperTheme}\>

\<CustomStatusBar

backgroundColor=\"transparent\"

// 4. Toggle icon colors based on theme

barStyle={theme.isDark ? \'light-content\' : \'dark-content\'}

/\>

{/\* App contents\... \*/}

\</PaperProvider\>

\</SafeAreaView\>

\</SafeAreaProvider\>

\</GestureHandlerRootView\>

);

### **💡 Best Practices for Future Reference**

- **Hydration Ordering is Critical:** Never calculate theme colors, user
  preferences, or tokens before your state manager (like Zustand or
  Redux) has finished hydrating from local storage. Doing so can cause
  flashes of the wrong theme or immediate app crashes.

- **Handle System Bars via the Parent Container:** The most reliable way
  to handle top notches and bottom navigation bars in React Native
  across different Android/iOS versions is to make the StatusBar
  component transparent and apply your theme\'s background color
  directly to the SafeAreaView wrapper.

- **One Component per File:** Always keep reusable UI components (like
  CustomStatusBar) in their own dedicated files rather than dumping them
  at the bottom of root files like App.tsx. This prevents export
  conflicts and keeps the codebase modular.

# Problem 38

Here is a summary of the navigation error we diagnosed, how to fix it,
and how to prevent it going forward.

## **The Error**

**\"The action \'GO_BACK\' was not handled by any navigator.\"**

This is a React Navigation development warning (which translates to a
silent failure or potential crash in production). It occurs when your
app tries to navigate back to a previous screen, but the navigation
stack history is completely empty. This usually happens if the screen
was opened via a deep link, a push notification, or if it\'s the very
first screen in a newly initialized nested navigator.

## **Related Files**

- CreatePost.tsx (specifically, the custom header implementation at the
  top of the file).

## **Code Snippets & Solution**

**The Problematic Code:**

The back button assumes there will always be a screen to return to,
calling goBack() blindly.

TypeScript

\<TouchableOpacity style={styles.headerLeftSection} onPress={() =\>
navigation.goBack()}\>

\<Icon source=\"arrow-left\" size={24} color={theme.colors?.text} /\>

\</TouchableOpacity\>

**The Solution:**

**Step 1: Add the import at the top of the file**

TypeScript

import { STACK_NAMES } from \'@/constants\'; // Or your specific
relative path

**Step 2: Update the onPress logic**

TypeScript

\<TouchableOpacity

style={styles.headerLeftSection}

onPress={() =\> {

if (navigation.canGoBack()) {

// Safe to go back

navigation.goBack();

} else {

// No history exists. Redirect to the Main Stack constant.

// This resolves to \'MainStack\', which is valid in your
RootStackParamList

navigation.navigate(STACK_NAMES.MAIN);

}

}}

\>

\<Icon source=\"arrow-left\" size={24} color={theme.colors?.text} /\>

\</TouchableOpacity\>

### **Summary of the rule for your project:**

Whenever you need a \"fallback\" home route from a screen that is part
of the **Root Stack**, always use **STACK_NAMES.MAIN** instead of the
string \'Home\'.

## **Best Practices to Avoid This in the Future**

1.  **Always Validate Navigation State:** Treat navigation.goBack() like
    a potentially dangerous operation. If a screen can ever be accessed
    directly (via deep links, notifications, or as the initial route of
    a tab/stack), always wrap the back action in an if
    (navigation.canGoBack()) check.

2.  **Define Fallback Routes:** When building standalone screens (like
    \"Create Post\", \"Settings\", or \"Profile\"), always decide what
    the default \"exit\" screen should be if the user arrived there
    without a natural navigation history.

3.  **Understand Nested Navigators:** If you put a Stack Navigator
    inside a Tab Navigator, each tab has its own separate history stack.
    Pressing \"back\" on the first screen of Tab B won\'t take you to
    Tab A; it will throw this exact error because Tab B\'s local stack
    is empty.

Would you like me to review how your app\'s root navigation is
structured to see if there are any other screens vulnerable to this
issue?

# Problem 39

## **Error Summary**

**Root Cause:** A **Nested Touchable Conflict**. The userInfo container
in PostCard.tsx was a TouchableOpacity with flex: 1. This created a
broad \"hit-box\" covering the entire top section of the card, hijacking
clicks intended for the main post detail navigation.

## **Solution Summary**

**Fix:** De-classified the broad header wrapper by changing it to a
standard View and applied targeted TouchableOpacity wrappers only to the
**Avatar** and **Username**. Added e.stopPropagation() to the community
link to prevent event bubbling to the main card.

## **Required Code Snippets**

#### **File: PostCard.tsx**

**1. Isolate Touch Targets in Header**

Replace the original userInfo block with specific touchable zones:

TypeScript

{/\* 1. Changed wrapper from TouchableOpacity to View \*/}

\<View style={styles.userInfo}\>

{/\* 2. Isolated touch target for Avatar \*/}

\<TouchableOpacity onPress={handleProfileNavigation}\>

{post?.user?.avatar_url ? (

\<Image source={{ uri: post.user.avatar_url }} style={styles.avatar} /\>

) : (

\<View style={styles.defaultAvatar}\>

\<Text style={styles.avatarText}\>

{pathOr(\'User\', \[\'user\', \'name\'\],
post)?.charAt(0)?.toUpperCase()}

\</Text\>

\</View\>

)}

\</TouchableOpacity\>

\<View style={styles.userTextContainer}\>

\<View style={styles.communityRow}\>

\<Text

onPress={(e) =\> {

e.stopPropagation(); // 3. Prevent triggering main card

handleCommunityNavigation();

}}

style={styles.communityName}

\>

{pathOr(\'\', \[\'community_name\'\], post) \|\| pathOr(\'\',
\[\'user\', \'prefix\'\], post)}

\</Text\>

\</View\>

{/\* 4. Isolated touch target for User Name \*/}

\<TouchableOpacity onPress={handleProfileNavigation}\>

\<Text style={styles.userName} numberOfLines={1}\>

{pathOr(\'\', \[\'user\', \'name\'\], post)}

\</Text\>

\</TouchableOpacity\>

\</View\>

\</View\>

**2. Main Card Navigation (Optional Logging)**

Update the root TouchableOpacity to verify navigation:

TypeScript

\<TouchableOpacity

style={\[styles.modernPostCard, \...\]}

onPress={() =\> {

console.log(\'Post Detail Triggered for ID:\', post.id);

handlePostClick(post.id);

}}

activeOpacity={0.8}

\>

{/\* Content \*/}

\</TouchableOpacity\>

Would you like me to help you adjust the spacing between these cards in
the Feed.tsx list next?

# Problem 40

![](data/media_dump/media/image12.png){width="0.651337489063867in"
height="1.1927088801399826in"}

Here is a complete summary of the blank screen transition bug and how we
solved it. This is perfect to drop into your project\'s documentation or
PR notes for future reference.

## **🐛 The Problem**

When navigating from the **Feed** to the **Post Detail** screen, users
experienced a brief, completely blank dark screen before the
PostDetailSkeleton loader appeared. The app was failing to render the
skeleton on the very first frame (Frame 1) of the screen transition.

## **📁 Files Involved**

- src/screens/community/PostDetail.tsx (Where the bug lived and was
  fixed)

## **🔍 Root Causes**

This was a multi-layered issue involving React state timing and React
Native UI thread bottlenecks:

1.  **State Logic Lag:** The original loading state required React
    Query\'s isPostFetching to be true. On the exact millisecond the
    screen mounts, the network request hasn\'t officially started, so
    isFetching was false. The app thought it didn\'t need the skeleton
    and tried to render empty data.

2.  **Stale Cache \"Empty Object\" Flash:** The hasData check was
    looking for the existence of a data object. If the cache briefly
    returned { data: {} }, it evaluated as true (skip skeleton),
    resulting in a blank render.

3.  **Android KeyboardAvoidingView Collapse:** Setting
    behavior=\"height\" on Android causes the view to dynamically
    calculate dimensions. On screen-mount, it doesn\'t know the height
    yet, causing the entire wrapper to collapse to 0 height.

4.  **Sticky Header Measurement Stall:** ScrollView halts the initial
    native UI paint when stickyHeaderIndices is active because it needs
    to calculate the exact height of the first child. With heavy
    skeleton animations, this calculation dropped the first frame.

## **🛠️ The Solution & Code Snippets**

#### **1. Strict Data Checking & State Logic Fix**

We modified the state logic to strictly check for the existence of the
post id, completely ignoring React Query\'s fetching state for the
initial render.

TypeScript

// ❌ BEFORE

const hasData = !!pathOr(undefined, \[\'data\'\], postDetailData);

const isInitialLoading = isPostFetching && !hasData;

// ✅ AFTER

// Strictly check for \'data.id\' to avoid false positives from empty
cached objects

const hasData = !!pathOr(undefined, \[\'data\', \'id\'\],
postDetailData);

const isInitialLoading = !hasData;

#### **2. Android Layout Collapse Fix**

We bypassed the KeyboardAvoidingView calculation bug on Android by
setting its behavior to undefined.

TypeScript

// ❌ BEFORE

\<KeyboardAvoidingView

behavior={Platform.OS === \'ios\' ? \'padding\' : \'height\'}

\>

// ✅ AFTER

\<KeyboardAvoidingView

// Prevent Android frame-1 layout collapse

behavior={Platform.OS === \'ios\' ? \'padding\' : undefined}

\>

#### **3. Native UI Thread Unblocking (Sticky Header Fix)**

We conditionally disabled the sticky header logic while the skeleton is
loading, allowing the UI thread to paint the skeleton instantly without
waiting to calculate sticky bounds.

TypeScript

// ❌ BEFORE

\<ScrollView

stickyHeaderHiddenOnScroll

stickyHeaderIndices={\[0\]}

\>

// ✅ AFTER

\<ScrollView

// Disable complex layout calculations during initial load to prevent
blank frame drops

stickyHeaderHiddenOnScroll={!isInitialLoading}

stickyHeaderIndices={!isInitialLoading ? \[0\] : undefined}

\>

Would you like me to help you document the \"nested touchables\" fix we
did in PostCard.tsx as well, or are you ready to move on to your next
ticket for this app?

//best practice

//implementing skeleton loader best practices:\
This is a great idea. Having a \"Skeleton Checklist\" in your project\'s
documentation or even a dedicated note file will save you hours of
debugging in the future.

## **📝 Note: Skeleton Loader Best Practices (Avoid the Blank Screen)**

To ensure a frame-1 instant paint and avoid the \"black/blank screen\"
flash during navigation, follow these technical guidelines whenever
creating a new skeleton:

## **1. The State Trigger (Strict Data Check)**

**Problem:** isFetching from React Query often starts as false for a
split second before the network request begins.

**Solution:** Always define isInitialLoading based on the absence of a
unique data ID, not the loading boolean.

- **Do:** const isInitialLoading = !companyData?.id;

- **Avoid:** const isInitialLoading = isFetching && !data;

## **2. Native Thread Unblocking (The Sticky Header Rule)**

**Problem:** ScrollView pauses rendering to calculate dimensions for
stickyHeaderIndices.

**Solution:** Dynamically disable sticky headers while the skeleton is
visible.

TypeScript

\<ScrollView

stickyHeaderIndices={!isInitialLoading ? \[0\] : undefined}

stickyHeaderHiddenOnScroll={!isInitialLoading}

\>

## **3. Layout Matching (The Blueprint Rule)**

**Problem:** If the skeleton is smaller or differently shaped than the
final UI, the screen will \"jump\" when data arrives.

**Solution:**

- Match **exact heights and widths** used in the real component.

- Match **spacing** (margins, padding, and gap).

- If the real screen uses a dark card (theme.colors.dialogBackground),
  the skeleton container must use it too.

## **4. Android Keyboard Stability**

**Problem:** KeyboardAvoidingView with behavior=\"height\" can collapse
to 0px height on the first frame on Android.

**Solution:** Disable the behavior for Android, as the OS handles it
natively better than the wrapper during transitions.

TypeScript

\<KeyboardAvoidingView behavior={Platform.OS === \'ios\' ? \'padding\' :
undefined}\>

## **5. Interaction Management (For Heavy Screens)**

**Best Practice:** If a screen has 20+ skeleton pieces, it can still
lag. Use InteractionManager to ensure the navigation animation finishes
before the heavy JS rendering starts.

TypeScript

useEffect(() =\> {

InteractionManager.runAfterInteractions(() =\> {

setCanRender(true);

});

}, \[\]);

## **🚀 Implementation Workflow**

1.  **Draft the Blueprint:** Look at the screenshot/design. Identify the
    3-4 main \"blocks\" (Header, Tabs, Content).

2.  **Assemble with Toolkit:** Use \<SkeletonBox /\> and \<SkeletonText
    /\> for everything.

3.  **Check Alignment:** Use alignItems: \'center\' in the parent if the
    elements are supposed to be centered (like your Post Cards).

4.  **Verify Frame 1:** Use console.log to ensure isInitialLoading is
    true on the very first log output.

Would you like me to save these details into a structured \"Developer
Guide\" markdown file for your team?

# Problem 41

Here is a complete summary of the issue and the fix for your project
documentation.

![](data/media_dump/media/image13.png){width="1.7353762029746282in"
height="3.7400339020122484in"}

## **The Problem**

A large, empty white space appeared below the Bottom Tab Navigator,
pushing the tab bar up and compressing the screen real estate. This was
caused by a **Safe Area Inset duplication** (double-padding).

Both the root-level \<SafeAreaView\> and the
\@react-navigation/bottom-tabs library were simultaneously applying
bottom padding to clear the device\'s bottom hardware bezels (like the
iOS home indicator), resulting in twice the necessary space.

## **The Files Involved**

- **App.tsx**: The actual culprit. This file contained the global
  \<SafeAreaView\> wrapper that forced bottom padding across the entire
  app.

- **MainNavigator.tsx**: The suspected file that was actually clean. It
  defines the bottom tabs, which automatically and correctly apply their
  own native safe area padding by default.

## **The Code: Before & After**

**Problematic Code Snippet (App.tsx):**

The edges prop included \'bottom\', forcing padding underneath the
NavigationContainer.

TypeScript

\<SafeAreaView

style={\[styles.container, { backgroundColor: appBackgroundColor }\]}

edges={\[\'top\', \'left\', \'right\', \'bottom\'\]} // \<\-- The root
cause

\>

\<PaperProvider theme={paperTheme}\>

{/\* \... \*/}

\<AppNavigator /\>

\</PaperProvider\>

\</SafeAreaView\>

**The Solution (App.tsx):**

Remove \'bottom\' from the edges array. This delegates the bottom
padding responsibility to the React Navigation library, which handles it
seamlessly for the tab bar.

TypeScript

\<SafeAreaView

style={\[styles.container, { backgroundColor: appBackgroundColor }\]}

edges={\[\'top\', \'left\', \'right\'\]} // \<\-- Fixed

\>

\<PaperProvider theme={paperTheme}\>

{/\* \... \*/}

\<AppNavigator /\>

\</PaperProvider\>

\</SafeAreaView\>

## **How to Avoid This in the Future**

- **Trust React Navigation:** By default, \@react-navigation/bottom-tabs
  and \@react-navigation/native-stack are built to handle device safe
  areas automatically. You rarely need to wrap navigators in a global
  SafeAreaView.

- **Use Insets for Granular Control:** Instead of using the
  \<SafeAreaView\> component globally, import the useSafeAreaInsets hook
  from react-native-safe-area-context inside individual screens. This
  allows you to add specific padding (like paddingBottom: insets.bottom)
  only exactly where it\'s needed, rather than blindly applying it to
  the whole app layout.

- **Check the Hierarchy:** If you see double headers or double padding,
  it almost always means two different layout wrappers in your component
  tree are trying to solve the same problem.

Would you like me to show you how to implement the useSafeAreaInsets
hook on your individual screens so your content doesn\'t get hidden
behind the tab bar?

# Problem 42\
![](data/media_dump/media/image9.png){width="1.671875546806649in"
height="3.6910476815398074in"}

Here is the updated summary reflecting your adoption of the
industry-standard best practice for handling system UI boundaries.

## **Issue Summary: Modal Content Overlapping System UI**

- **The Problem:** The content inside your event filter modal was
  overflowing into the device\'s safe display areas. The header was
  rendering underneath the top status bar/notch, and the bottom buttons
  were overlapping with the device\'s navigation bar (gesture controls).

- **Why it Happened:** You were using a standard \<View\> as the root
  container inside a \<Modal\> with the statusBarTranslucent prop set to
  true. Standard View components stretch to the absolute edges of the
  screen and do not account for physical device cutouts (like notches or
  dynamic islands) or OS-level navigation overlays.

- **File Modified:** src/screens/events/EventFiltersModal.tsx

## **The Solution: react-native-safe-area-context**

Instead of relying on React Native\'s built-in (and sometimes
inconsistent) SafeAreaView, we implemented the industry-standard
react-native-safe-area-context library.

By using the useSafeAreaInsets hook, the app dynamically detects the
exact pixel measurements of the device\'s top notch/status bar and
bottom navigation bar, applying them directly as padding to standard
\<View\> components. This guarantees a pixel-perfect layout across all
Android and iOS devices, regardless of screen shape or OS navigation
settings.

#### **1. Updated Imports**

We removed the standard SafeAreaView and imported the hook from the
context library:

JavaScript

import {

Modal,

View,

Text,

StyleSheet,

TouchableOpacity,

TouchableWithoutFeedback,

TextInput,

} from \'react-native\';

import { useSafeAreaInsets } from \'react-native-safe-area-context\'; //
\<\-- Hook added

#### **2. Fetching the Insets**

Inside the component, we called the hook to grab the device-specific
pixel boundaries:

JavaScript

const EventFiltersModal: React.FC\<EventFiltersModalProps\> = ({ /\*
props \*/ }) =\> {

// Grabs exact pixel sizes for the specific device running the app

const insets = useSafeAreaInsets();

// \...

#### **3. Updated Render Block (Applying Dynamic Padding)**

We applied those specific inset values to the top and bottom padding of
the root \<View\> container:

*Before:*

JavaScript

\<TouchableWithoutFeedback onPress={handleCancel}\>

\<View style={styles.overlay}\>

\<TouchableWithoutFeedback\>

{/\* Modal Content \*/}

\</TouchableWithoutFeedback\>

\</View\>

\</TouchableWithoutFeedback\>

*After:*

JavaScript

\<TouchableWithoutFeedback onPress={handleCancel}\>

\<View style={\[

styles.overlay,

// Pushes content down past the notch and up past the gesture bar

{ paddingTop: insets.top, paddingBottom: insets.bottom }

\]}\>

\<TouchableWithoutFeedback\>

{/\* Modal Content \*/}

\</TouchableWithoutFeedback\>

\</View\>

\</TouchableWithoutFeedback\>

## **Verification**

The logs successfully confirmed the fix is working, actively detecting
the safe areas on the device (e.g., Applying Safe Area Insets: Top:
44.44px, Bottom: 24.17px). Because these numbers are registering, it
also confirms your app is correctly wrapped in a \<SafeAreaProvider\>
higher up in the navigation tree.

# Problem 43

## **Summary of Issue and Resolution**

## **1. The Problem**

There were two distinct issues occurring simultaneously in the \"My
Upcoming Events\" screen:

- **UI/UX Bug (Focus Loss):** Whenever the user typed in the search bar,
  the keyboard would abruptly close after 500ms. This happened because
  the component\'s loading logic replaced the entire screen (including
  the active SearchBar) with a Skeleton placeholder, forcing the input
  to unmount and lose focus.

- **Functional Bug (Filtering Failure):** Even when the user typed fast
  enough, the list wouldn\'t filter. Logs revealed that the backend
  endpoint for \"My Events\" (events/me) was ignoring the search
  parameter and returning the full list of events regardless of the
  query.

## **2. Relevant Code Files**

- **EventList.tsx:** The primary file where the SearchBar UI, the
  useEventsInfiniteQuery hook, and the event list rendering logic
  reside.

- **useEvents.ts & event.service.ts:** The API layer where the network
  requests are constructed.

- **UpcomingEvents.tsx:** A separate component used for the horizontal
  home-screen carousel (not where the search bar logic lived).

## **3. Key Code Snippets & Modifications**

#### **The UI Fix (Preventing Keyboard Closure)**

We removed the early return that was unmounting the SearchBar.

**Before:**

TypeScript

if (isLoading) {

return \<View\>\<EventListSkeleton /\>\</View\>; // Replaces everything!

}

**After:**

We moved the condition inside the main return so it only affects the
list area:

TypeScript

{isLoading && eventsList.length === 0 ? (

\<EventListSkeleton /\>

) : (

\<FlatList \... /\>

)}

#### **The Logic Fix (Enabling Search Results)**

We added a manual frontend filter in the useMemo block to handle
instances where the backend doesn\'t support search filtering.

TypeScript

const eventsList = useMemo(() =\> {

// \... existing unique events logic

let finalEvents = Array.from(uniqueEvents.values());

if (debouncedSearchQuery.trim()) {

const query = debouncedSearchQuery.toLowerCase();

finalEvents = finalEvents.filter(event =\>

event.title?.toLowerCase().includes(query)

);

}

return finalEvents;

}, \[eventsData, selectedFilter, debouncedSearchQuery\]);

## **4. The Final Solution**

The solution involved **stabilizing the UI tree** and **supplementing
the API**. By ensuring the SearchBar stays mounted during loading
states, the keyboard remains open. By adding a local .filter() pass on
the returned data, the search functionality works immediately, even if
the backend is non-responsive to the search query.

## **5. Best Practice: The \"Stable Input\" Pattern**

To avoid these issues in future React Native or React development,
follow these principles:

- **Stable Component Lifecycles:** Never unmount a parent container of a
  TextInput during a loading or error state. The input should remain in
  the DOM/UI Tree to maintain focus.

- **Granular Loading States:** Use \"inline\" skeletons or loading
  indicators for the data-driven parts of the UI, rather than
  \"page-level\" skeletons that reset the user\'s interaction state.

- **Backend-Frontend Parity:** While filtering should ideally happen on
  the backend, always implement a lightweight frontend filter for \"My
  Items\" lists. It provides a \"zero-latency\" feel for the user and
  acts as a safeguard against inconsistent API behaviors.

**//postman debugging steps:\**
This is a great idea. Having a \"Bug Report\" or a \"Test Protocol\"
saved will make you look very professional when you present this to the
backend team.

Here is the reference sheet for the steps you took to isolate the bug.

## **🛠 Bug Investigation Reference: Event Registration Sync**

**Issue:** Events remain in the \"Upcoming Events\" list even after a
successful cancellation.

**Root Cause:** Backend API (/events/me) returns stale data (Eventual
Consistency/Caching issue) immediately following a DELETE request.

## **📍 API Configuration**

- **Base URL:** https://api.chiiro.co/api/v1

- **Auth Type:** Bearer Token (JWT)

## **🧪 Postman Test Protocol (The Proof)**

#### **Step 1: The Baseline (Verify current state)**

- **Endpoint:** GET /events/me

- **Action:** Retrieve the list of events you are currently registered
  for.

- **Goal:** Find the id of the event you intend to cancel (e.g., id:
  69).

- **Note:** If the event isn\'t here, you aren\'t registered for it yet.

#### **Step 2: The Action (Cancel the registration)**

- **Endpoint:** DELETE /events/{{EVENT_ID}}/register

- **Action:** Send a DELETE request to the specific registration
  endpoint.

- **Goal:** Receive a 200 OK or success: true response with the message
  \"Registration cancelled\".

- **Observation:** This confirms the server *acknowledged* the request
  to delete.

#### **Step 3: The Verification (The \"Smoking Gun\")**

- **Endpoint:** GET /events/me

- **Action:** **Immediately** (within 1-2 seconds) call the list
  endpoint again.

- **Goal:** Check if the {{EVENT_ID}} used in Step 2 is still present in
  the JSON array.

- **Result:** If the ID is still present, the backend is serving **stale
  data**.

## **📝 Key Terms for the Backend Team**

When you talk to the developers, use these terms to describe what you
found:

1.  **Race Condition:** When the \"Read\" request happens so fast that
    the \"Write\" (the deletion) hasn\'t finished yet.

2.  **Stale Cache:** The server is likely serving a \"saved copy\"
    (Redis/Cache) of your event list instead of looking at the live
    database.

3.  **Eventual Consistency:** A database state where changes take time
    to propagate across all systems.

## **💡 Best Practices for Future Prevention**

- **Cache Invalidation:** The backend should automatically \"purge\" or
  delete the user\'s cached event list the moment a DELETE or POST
  registration request succeeds.

- **Optimistic UI (Frontend):** On the frontend, we can manually hide
  the card the moment the user clicks \"Confirm,\" but the backend
  **must** eventually provide the correct data to ensure the card
  doesn\'t \"pop back\" on a refresh.

# Problem 44

That was quite a marathon session, but you've successfully bridged the
gap between your API and your UI! You transformed a static filter into a
dynamic, location-aware system.

Here is the comprehensive summary of all the issues resolved and the
current state of your code.

## **🛠️ Phase 1: The Infrastructure (Resolved Earlier)**

**Files Affected:** EventFiltersModal.tsx, EventList.tsx

## **1. The API & State Disconnect**

- **Problem:** The filter originally only supported a single category.
  Location was a plain string that didn\'t talk to the backend
  effectively.

- **Solution:** Integrated the useAutoCompleteLocation hook. Updated the
  FilterState interface to handle an object containing categoryId,
  timeframe, and locationId.

- **Result:** The parent component now constructs a precise API payload
  for useEventsInfiniteQuery.

## **2. Keyboard & Scroll UX Fixes**

- **Problem:** The modal was hidden behind the keyboard, and the
  autocomplete dropdown was cut off and unscrollable.

- **Solution:** \* Wrapped the modal in \<KeyboardAvoidingView\>.

  - Swapped the container \<View\> for a \<ScrollView\> with
    keyboardShouldPersistTaps=\"handled\".

- **Result:** Users can now actually see and tap the location
  suggestions.

## **🏗️ Phase 2: The Logic Sync (Just Resolved)**

**Files Affected:** EventFiltersModal.tsx, EventList.tsx

## **3. The ID vs. Label Mismatch**

- **Problem:** When you filtered by \"Kolkata\", the API received ID 7.
  The local filter tried to find the character \"7\" in the word
  \"Kolkata\", resulting in \"No Events Available.\"

- **Solution:** Introduced selectedLocationName to separate the **API
  ID** from the **UI Display Label**.

**Code Snippet (State Update in EventList.tsx):**

TypeScript

const \[selectedLocationId, setSelectedLocationId\] = useState\<string
\| number \| null\>(null);

const \[selectedLocationName, setSelectedLocationName\] =
useState\<string \| null\>(null);

## **4. Local Filtering Logic**

- **Problem:** The list didn\'t always refresh instantly or correctly
  match city names.

- **Solution:** Refined the eventsList useMemo to search for the
  selectedLocationName string within the event\'s city or address
  fields.

**Code Snippet (Logic in EventList.tsx):**

TypeScript

if (selectedLocationName) {

finalEvents = finalEvents.filter(event =\> {

const eventCity = pathOr(\'\', \[\'location\', \'city\'\],
event).toLowerCase();

const filterText = selectedLocationName.toLowerCase();

return eventCity.includes(filterText);

});

}

## **🚀 Phase 3: The UI (Current Status)**

**Files Affected:** EventList.tsx

## **5. Active Filter Chips**

- **Problem:** The user couldn\'t see what filters were active without
  opening the modal.

- **Solution:** Added a horizontal ScrollView below the SearchBar that
  maps the active states to visual chips with \"Clear\" buttons.

**The Final Payload Structure:**

TypeScript

// Shared across both files

export interface FilterState {

categoryId: string \| null;

timeframe: string \| null;

locationId: string \| number \| null;

locationName?: string \| null; // The hero of Phase 2

}

## **✅ Summary of Current Working State**

1.  **Modal:** Correctly captures IDs for the API and Names for the UI.

2.  **Parent:** Receives the full filter object, updates the API
    request, and locally filters the results for immediate feedback.

3.  **UI:** Displays chips (e.g., \"7 Days\", \"Kolkata\") that allow
    users to see and remove filters instantly.

**Would you like me to help you style the \"Empty State\" (No Events
Found) to include a \"Clear All Filters\" button for a better user
experience?**

# Problem 45

Here is a complete summary of the Settings screen layout issue, the
solution, and the architectural takeaways for your project\'s
documentation.

## **Issue Summary: Navigation Bar Overlap on Settings Screen**

**The Problem:**

On certain Android devices, the \"Logout\" button at the very bottom of
the SettingsScreen was being partially or completely hidden underneath
the OS-level system navigation bar (specifically on devices using the
classic 3-button software navigation).

**The Root Cause:**

1.  **Static Padding:** The ScrollView containing the settings list
    relied on a hardcoded bottom padding (theme.spacing.xl). While this
    looked fine on devices with thin gesture indicators (like iOS or
    modern Androids), it was insufficient to clear the height of thicker
    software navigation bars.

2.  **Variable Scope Error (During Fix):** An initial attempt to use
    useSafeAreaInsets() failed because the hook was accidentally
    declared inside a child component (SettingItem), making the insets
    variable invisible and undefined to the parent SettingsScreen where
    the ScrollView was located.

**File Involved:** \* SettingsScreen.tsx (containing both SettingItem
and SettingsScreen components).

## **The Code Fix**

To resolve the issue, the useSafeAreaInsets hook was moved to the
correct component scope, and its value was dynamically added to the
ScrollView\'s padding.

**1. Moving the Hook to the Correct Scope:**

The hook was removed from the SettingItem component and placed at the
absolute top of the SettingsScreen component.

JavaScript

// ✅ CORRECT PLACEMENT

export const SettingsScreen: React.FC = () =\> {

const { t } = useTranslation();

const theme = useTheme();

// Hook declared at the top level of the component using it

const insets = useSafeAreaInsets();

const { changeLanguage, supportedLanguages, currentLanguage: language }
= useLanguage();

// \... rest of state

**2. Dynamic ScrollView Padding:**

The ScrollView was updated to dynamically inject the device\'s specific
bottom inset value, plus a small visual buffer (20), ensuring the
content always scrolls safely above the navigation UI.

JavaScript

// ✅ DYNAMIC PADDING IMPLEMENTATION

\<ScrollView

style={styles.container}

contentContainerStyle={\[

styles.scrollContent,

// theme.spacing.xl (Base padding) + insets.bottom (OS Nav Bar Height) +
20 (Visual breathing room)

{ paddingBottom: theme.spacing.xl + (insets?.bottom \|\| 0) + 20 }

\]}

\>

{/\* Settings Content\... \*/}

\</ScrollView\>

## **Best Practices for Future Reference**

To prevent similar UI bugs and React rendering errors in the future,
keep these two rules in mind:

- **Handling Safe Areas in Scrollable Lists:** Whenever you have a
  ScrollView or FlatList that reaches the bottom edge of the screen,
  **never rely on static padding**. Always use insets.bottom dynamically
  inside the contentContainerStyle. This allows the list to scroll
  naturally behind the transparent navigation bar, while ensuring the
  actual content (like the last list item) stops safely above it.

- **The Golden Rule of React Hooks:** Hooks (like useState, useTheme, or
  useSafeAreaInsets) must be declared at the **very top level** of the
  specific React functional component that needs to consume their data.
  If a parent component (like SettingsScreen) needs a value, you cannot
  declare the hook inside a child component (like SettingItem) and
  expect the parent to see it.

# Problem 46

## **Problem**

A small white dot briefly flashed at the top of the screen whenever
navigating to the Events screen.

**Root Cause:** The RefreshControl component was tied directly to React
Query\'s isRefetching state. Because useFocusEffect triggers queries to
refetch in the background every time the screen comes into focus,
isRefetching became true. This forced the native Android pull-to-refresh
spinner to attempt to render programmatically without an actual physical
swipe gesture, causing it to glitch and display as a static white dot.

## **File**

Events.tsx

## **Solution**

Decouple the RefreshControl from the background fetching state. By
introducing a dedicated local state (isManualRefresh) and wrapping the
query refetches in a try/finally block inside an asynchronous onRefresh
function, the spinner is restricted to only activate during a physical
pull-down gesture. Screen navigation now refetches data silently in the
background without triggering the UI glitch.

## **Code Snippets**

**1. Added local state:**

TypeScript

const \[isManualRefresh, setIsManualRefresh\] = useState(false);

**2. Updated the refresh handler to manage the new state
asynchronously:**

TypeScript

const onRefresh = useCallback(async () =\> {

setIsManualRefresh(true);

try {

await Promise.all(\[

refetchUpcoming(),

refetchOther(),

refetchCategories(),

\]);

} finally {

setIsManualRefresh(false);

}

}, \[refetchUpcoming, refetchOther, refetchCategories\]);

**3. Bound RefreshControl to the new state:**

TypeScript

\<RefreshControl

refreshing={isManualRefresh} // Changed from isRefetching

onRefresh={onRefresh}

tintColor={theme.colors.primary}

colors={\[theme.colors.primary\]}

/\>

# Problem 47

Inconsistent border radius of search inputs in company profile-\>create
job-\>new opportunity screen

This is a great idea. Keeping a \"dev log\" of these styling fixes saves
a lot of time when you build new screens. Here is the summary of our
session for your records.

## **Project Reference: Input Styling Consistency**

## **1. Files Involved**

We examined the following files to trace the styles and apply the fix:

- **CreateJob.tsx**: The main screen implementation where the form is
  built.

- **src/components/forms/FormInput.tsx**: The entry point/dispatcher
  that renders the specific field types.

- **src/components/forms/TextInputField.tsx**: The component for
  standard text entries (e.g., Job Title).

- **src/components/forms/AutocompleteField.tsx**: The component for
  dropdowns and search-based selects (e.g., Job Type, Location).

- **src/components/forms/DatePickerField.tsx**: The component for date
  and time selection.

- **src/components/forms/shared/styles.ts**: The shared style sheet used
  by multiple form components.

- **src/theme/spacing.ts**: The source of truth for borderRadius and
  spacing values.

## **2. The Problem**

The \"New Opportunity\" screen had three distinct UI inconsistencies:

1.  **Mismatched Radii:** The TextInputField was using borderRadius.sm
    (\$4\$px), while the Autocomplete and Date fields were using
    borderRadius.md (\$8\$px).

2.  **Sharp Top Corners:** Because TextInputField uses React Native
    Paper\'s flat mode, it automatically forced the top corners to \$0\$
    radius, even when a borderRadius was provided.

3.  **Dropdown Search Style:** The search bar inside the Autocomplete
    modal used a \"bottom-line\" border style, which didn\'t match the
    \"boxed\" style of the main form.

## **3. The Solution**

#### **Step A: Standardize the Radius**

We updated TextInputField.tsx to use theme.borderRadius.md instead of sm
to match the other components.

#### **Step B: Fix the \"Flat Mode\" Top Corners**

In TextInputField.tsx, we manually forced the top corners to be rounded
by adding specific style properties to the TextInput component:

TypeScript

borderTopLeftRadius: theme.borderRadius.md,

borderTopRightRadius: theme.borderRadius.md,

#### **Step C: Unify the Internal Search Bar**

In AutocompleteField.tsx, we redefined the searchContainer to match the
main input boxes:

- Changed borderBottomWidth to a full borderWidth: 1.

- Added borderRadius: theme.borderRadius.md.

- Added marginHorizontal and height to make it a floating \"box\" rather
  than a full-width line.

## **Final Configuration Table**

  -----------------------------------------------------------------------
  **Component**      **Border       **Border      **Mode / Style**
                     Radius**       Width**       
  ------------------ -------------- ------------- -----------------------
  **TextInput**      md (\$8\$px)   \$1\$         Flat (with top-radius
                                                  override)

  **Autocomplete**   md (\$8\$px)   \$1.5\$       Boxed Trigger

  **DatePicker**     md (\$8\$px)   \$1\$         Boxed Touchable

  **Modal Search**   md (\$8\$px)   \$1\$         Boxed Container
  -----------------------------------------------------------------------

# Problem 48

Here is a summary of the problem and the solution for your records.

## **File Reference**

CreatePost.tsx (React Native component)

## **The Problem**

1.  **Validation Logic Flaw:** The \"Post\" (send) button was becoming
    active and clickable as soon as a community was selected, ignoring
    whether the required text fields (title and bodyText) were empty.

2.  **Styling Issue:** Even when the button was functionally enabled,
    the paper-plane icon remained a static grey color instead of turning
    orange (the theme\'s primary color) to indicate it was ready.

## **The Solution**

1.  **Form State Integration:** Configured react-hook-form to validate
    inputs as the user types (mode: \'onChange\') and extracted its
    built-in isValid boolean. Added this boolean to the isPostDisabled
    condition.

2.  **Dynamic Icon Tinting:** Applied a conditional tintColor to the
    button\'s \<Image\> component, forcing the icon to render in
    theme.colors.primary when enabled and \'gray\' when disabled.

## **Code Snippets: Before & After**

#### **1. Form Hook Setup**

**Before:**

TypeScript

const {

control,

handleSubmit,

setValue,

watch,

reset,

formState: { errors },

} = useForm\<FormData\>({

defaultValues: {

title: \'\',

bodyText: \'\',

tags: \[\],

document: null,

},

});

**After:**

TypeScript

const {

control,

handleSubmit,

setValue,

watch,

reset,

formState: { errors, isValid }, // \<\-- Added isValid

} = useForm\<FormData\>({

mode: \'onChange\', // \<\-- Added mode to validate on typing

defaultValues: {

title: \'\',

bodyText: \'\',

tags: \[\],

document: null,

},

});

#### **2. Disabled State Logic**

**Before:**

TypeScript

const isPostDisabled = !selectedCommunity \|\| postCreationLoading \|\|
documentUploadLoading;

**After:**

TypeScript

const isPostDisabled = !selectedCommunity \|\| !isValid \|\|
postCreationLoading \|\| documentUploadLoading; // \<\-- Added !isValid

#### **3. Button Image Styling**

**Before:**

TypeScript

\<Image

source={require(\'../../assets/post.png\')}

style={{

width: 20,

height: 20,

opacity: isPostDisabled ? 0.5 : 1,

}}

resizeMode=\"contain\"

/\>

**After:**

TypeScript

\<Image

source={require(\'../../assets/post.png\')}

style={{

width: 20,

height: 20,

opacity: isPostDisabled ? 0.5 : 1,

tintColor: isPostDisabled ? \'gray\' : theme.colors.primary, // \<\--
Added conditional tintColor

}}

resizeMode=\"contain\"

/\>

# Problem 49

**NOTIFICATIONS NOT WORKING EVEN WHEN TOGGLED ON OR OFF**

The issue is a **disconnect between your frontend database state and the
OneSignal device state.**

## **The Root Cause**

1.  In SettingsScreen.tsx, when you toggle the push notification switch,
    your app successfully updates your backend database (as shown in
    your backend teammate\'s screenshot).

2.  **However, you never tell the actual phone to stop receiving push
    notifications.** 3. In your src/services/onesignal.ts file, you
    correctly built the optOut() and optIn() methods. But if you look
    closely at your SettingsScreen.tsx, **you are never calling them.**

3.  Because the OneSignal SDK on the device remains active and
    subscribed, it will continue to catch and display any notification
    sent to it. (This also implies your backend is likely blindly
    sending push payloads to OneSignal without checking the
    enablePushNotification database flag first).

## **How to Fix It**

You need to call your OneSignal optIn and optOut methods immediately
after a successful API update in your SettingsScreen.tsx.

Here is the exact code change required for SettingsScreen.tsx.

**1. Add the import at the top of the file:**

TypeScript

import OneSignalService from \'@/services/onesignal\'; // adjust the
path based on your folder structure

**2. Update the handleToggleNotification function:**

TypeScript

const handleToggleNotification = async (type: \'push\' \| \'email\',
value: boolean) =\> {

try {

const payload =

type === \'push\'

? { enablePushNotification: value }

: { enablePromotionalNotification: value };

await updateSettingsMutation.mutateAsync(payload);

// \-\-- ADD THIS BLOCK \-\--

// Sync the OneSignal SDK state with the user\'s preference

if (type === \'push\') {

if (value) {

OneSignalService.getInstance().optIn();

} else {

OneSignalService.getInstance().optOut();

}

}

// \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\--

// Generate the dynamic success message

const notificationType = type === \'push\' ? \'Push\' : \'Email\';

const actionText = value ? \'enabled\' : \'disabled\';

toast.success(\`\${notificationType} notifications \${actionText}
successfully.\`);

} catch (err) {

console.error(err);

toast.error(t(\'error\'));

}

};

## **What to tell your Backend Teammate**

While this frontend fix will stop the device from displaying the
notifications, you should tell your backend teammate:

> *\"The app\'s UI was saving the setting to the DB, but failing to
> opt-out the device via the OneSignal SDK. However, the backend should
> also be checking if enablePushNotification === true in the database
> BEFORE triggering the OneSignal API. Right now, it looks like the
> backend is sending the push payload regardless of what the user\'s DB
> setting is.\"*

Here is a quick summary of how you tested the OneSignal push
notification fix using your emulator and dev tools. You can save this
for future reference:

## **🧪 Testing OneSignal Push Toggles (Emulator & Dev Tools)**

**Objective:** Verify that the frontend UI switch correctly triggers the
OneSignal SDK (optIn / optOut) and successfully syncs with the backend
database.

**1. Setup**

- Run the app on your Android Emulator.

- Open your Metro Bundler terminal or React Native Debugger to watch the
  console logs.

- Navigate to the **Settings** screen in the app.

**2. Execution & Network Verification**

- Toggle the Push Notifications switch **ON** and **OFF**.

- Look at your terminal logs. You should see your API successfully
  sending the payload and returning a success response:

  - 🚀 API Request: {method: \'PUT\', url: \'/settings/notifications\',
    \...}

  - ✅ API Response: {status: 200, url: \'/settings/notifications\',
    \...}

  - *This proves the frontend state is successfully updating the backend
    database.*

**3. Verifying the OneSignal SDK Trigger**

- When you toggle the switch to **ON** (optIn is called), watch the
  emulator screen.

- **The OS-Level Proof:** If your emulator\'s system-level notifications
  are turned off, Android will immediately intercept the OneSignal SDK
  and throw a native warning modal: *\"Notifications Not Available - You
  have previously denied Notifications.\"* \* *This modal is the
  absolute proof that your UI switch is successfully talking to the
  OneSignal SDK.*

- To fix the modal and test actual delivery, click **SETTINGS** on that
  popup and allow notifications at the Android OS level.

**4. The Final End-to-End Test (Real-world scenario)**

- **Test Opt-Out:** Toggle the switch **OFF** in the app. Have a
  teammate send you a chat message or connection request. Verify nothing
  shows up on your emulator screen.

- **Test Opt-In:** Toggle the switch **ON**. Have a teammate send
  another message. Verify the push notification successfully appears on
  the emulator.

# Problem 50

## **The Problem**

When clicking on certain job cards (\"Pit Crew\" and \"Mobile App Dev\")
and navigating to the company profile, the app crashed with \"Render
Errors.\"

- **Why it happened:** The crashes were data-dependent. \"Pit Crew\" had
  company documents, which triggered the rendering of DocumentsTab.tsx.
  \"Mobile App Dev\" had followers, which triggered FollowersTab.tsx.

- **The Root Cause:** Both of these tab files were trying to use
  functions (getFileIcon, formatFileSize) or UI components
  (FollowerItem) that were completely missing from the files and were
  not imported from anywhere else in your project. React Native doesn\'t
  know what to render when a referenced variable doesn\'t exist, so it
  fatally crashes.

## **The Solution**

We defined the missing helper functions and UI components directly
inside their respective files so that the app had the actual code to
execute when those tabs were rendered.

## **1. File: DocumentsTab.tsx**

**Before:** The code tried to use getFileIcon and formatFileSize without
them being defined anywhere.

TypeScript

// BEFORE: Missing definitions caused a crash here

const extension = document.extension \|\|
documentName.split(\'.\').pop() \|\| \'\';

const iconName = getFileIcon(extension, document.mimeType);

const fileSize = formatFileSize(document.size);

**After:** We added the explicit logic for both functions right above
the DocumentItem component.

TypeScript

// AFTER: Functions defined before they are used

const getFileIcon = (extension: string, mimeType?: string) =\> {

const ext = extension.toLowerCase();

if (\[\'pdf\'\].includes(ext)) return \'file-pdf-box\';

// \... other extensions

return \'file-document-outline\';

};

const formatFileSize = (bytes?: number) =\> {

if (!bytes \|\| bytes === 0) return \'\';

const k = 1024;

const sizes = \[\'Bytes\', \'KB\', \'MB\', \'GB\'\];

const i = Math.floor(Math.log(bytes) / Math.log(k));

return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + \' \' +
sizes\[i\];

};

const DocumentItem: React.FC\<DocumentItemProps\> = ({ \... }) =\> {

// \...

## **2. File: FollowersTab.tsx**

**Before:** The file had a placeholder comment but no actual component,
crashing when the loop tried to map over the followers list.

TypeScript

// BEFORE: The component was missing entirely

// \... (Follower Interface and FollowerItem Component remain unchanged)

// Later in the render block:

return (

\<FollowerItem // CRASH: \"Property \'FollowerItem\' doesn\'t exist\"

key={key}

follower={follower}

// \...

/\>

);

**After:** We wrote the full FollowerItem UI component and placed it in
the file so the loop had something to render.

TypeScript

// AFTER: Component fully defined

interface FollowerItemProps {

follower: any;

theme: any;

styles: any;

onPress: (follower: any) =\> void;

onConnect: (userId: string \| number) =\> void;

}

const FollowerItem: React.FC\<FollowerItemProps\> = ({ follower, theme,
styles, onPress, onConnect }) =\> {

// \... UI layout with TouchableOpacity, Text, and Icons

};

## **Best Practices to Avoid This in the Future**

1.  **Pay Attention to IDE Warnings (Squiggly Lines):** Modern editors
    like VS Code will underline missing variables or components in red.
    If you see a red line under a function name, **do not run the app**.
    Fix the missing import or definition first. A runtime crash is
    almost guaranteed if your editor is throwing a \"Cannot find name\"
    TypeScript error.

2.  **Use a Strict Linter (ESLint):\**
    Ensure your ESLint rules are configured to block builds if there are
    no-undef (undefined variables) errors. This forces you to catch
    missing components during the coding phase rather than testing on a
    device.

3.  **Modularize Shared Logic:\**
    While putting getFileIcon inside DocumentsTab.tsx works perfectly, a
    better long-term practice is to put highly reusable functions into
    your src/utils/helpers.ts file and export them. That way, if you
    ever need to show a file icon on a completely different screen (like
    a chat screen), you don\'t have to rewrite the logic.

4.  **Create a Dedicated Components Folder:\**
    Similarly, if FollowerItem is going to be used anywhere else in your
    app, it should be moved out of FollowersTab.tsx and into a dedicated
    file like src/components/FollowerItem.tsx. You would then just
    import { FollowerItem } from \'@/components\' at the top of your
    tabs.

# Problem 51

It's great to see the app is finally running! Merging branches often
feels like a game of \"whack-a-mole\" with configuration files, but
you\'ve cleared the biggest hurdles.

Here is a summary of the issues you faced and the steps you took to
resolve them.

## **🛠 Summary of Actions Taken**

## **1. Upgraded the Android SDK**

You encountered a build failure because a library dependency (likely
from Firebase) moved to a version that required the latest Android 16
(Baklava) tools.

- **Action:** Modified android/build.gradle to set compileSdkVersion and
  targetSdkVersion to **36**.

- **Action:** Updated buildToolsVersion to **36.0.0**.

- **Action:** Used the Android Studio SDK Manager to install the
  **Android 16.0 (API 36.1)** platform and build tools.

## **2. Resolved Versioning Conflicts**

After fixing the build, the emulator refused to install the new APK
because it already had a version of the app with a higher \"Version
Code\" than what you were building.

- **Action:** Modified android/app/build.gradle.

- **Action:** Bumping the versionCode to **17** (to match the existing
  install) or higher, and updated the versionName to **1.0.2**.

## **📖 Error Reference for Your Logs**

If you see these again, here is what they mean in \"human\" terms:

  ---------------------------------------------------------------------
  **Error Name**                           **What it actually means**
  ---------------------------------------- ----------------------------
  **CheckAarMetadataWorkAction**           **SDK Mismatch:** One of
                                           your libraries is \"too
                                           new\" for your current
                                           Android SDK settings. You
                                           must upgrade your compileSdk
                                           to the version requested in
                                           the error.

  **INSTALL_FAILED_VERSION_DOWNGRADE**     **Version Block:** The
                                           emulator has a newer version
                                           of the app than the one you
                                           just built. You must either
                                           **uninstall** the app from
                                           the emulator or **increase**
                                           the versionCode in
                                           app/build.gradle.
  ---------------------------------------------------------------------

## **Pro-Tip for Mac Developers**

Since you are on a **MacBook Air**, sometimes the build cache can get
\"sticky\" after a major SDK change or a branch merge. If you ever see
weird, unexplainable Java errors in the future, run this \"nuke\"
command to start fresh:

Bash

watchman watch-del-all && rm -rf node_modules && yarn install && cd
android && ./gradlew clean && cd .. && yarn android

**Would you like me to show you a script you can add to your
package.json to handle this cleanup automatically in one command?**

# Problem 52

**Making the button 'View All' beside Recommended Communities and Job
Opportunities section not bold:**

To help you keep track of these changes, here is a summary of how we
resolved the **\"View All\" bold text issue** while protecting the
shared component\'s integrity.

## **The Problem**

The SectionHeader component had the fontWeight: \'bold\' and fontFamily:
theme.fonts.families.bold properties hardcoded into its internal
stylesheet. Because this was a shared component, changing it directly
would have affected every header in the app.

## **The Resolution**

We implemented a **Prop-Based Override**. This allowed specific screens
to \"tell\" the header to look different without changing the default
behavior for other screens.

#### **1. Shared Component Update**

**File:** SectionHeader.tsx

We updated the SectionHeaderProps interface to include viewAllTextStyle
and applied it using an array-style override on the Text component.

TypeScript

// Updated Interface

interface SectionHeaderProps {

// \... other props

viewAllTextStyle?: object;

}

// Updated Component Logic

\<Text style={\[styles.viewAll, viewAllTextStyle\]}\>

{viewAllText \|\| t(\'action.viewall\')}

\</Text\>

#### **2. Screen-Specific Implementations**

By passing the override prop from the parent files, the \"View All\"
text was switched to a normal weight and the regular font family.

**File:** RecommendedCommunities.tsx

JavaScript

\<SectionHeader

title={\`\${t(\'common.recommended\')} \${t(\'common.communities\')}\`}

onViewAll={() =\> navigation.navigate(\'CommunityList\')}

viewAllTextStyle={{

fontWeight: \'normal\',

fontFamily: theme.fonts.families.regular,

}}

/\>

**File:** JobOpportunities.tsx

JavaScript

\<SectionHeader

title=\"Job Opportunities\"

onViewAll={() =\> {

navigation.navigate(SCREEN_NAMES.JOB_POSTINGS);

}}

viewAllTextStyle={{

fontWeight: \'normal\',

fontFamily: theme.fonts.families.regular,

}}

/\>

## **Why this worked**

This approach followed a \"surgical\" fix strategy:

- **Encapsulation:** The logic for \"normal\" text stays within the
  screens that actually want it.

- **Backward Compatibility:** Any other screen using SectionHeader that
  doesn\'t pass this new prop will still see the original bold text,
  preventing any accidental UI breaks elsewhere.

# Problem 53

Here is a clear and structured summary of the issue and solution that
you can keep for your documentation.

## **Bug Fix Reference: App Crash on Event Card Press**

**Problem Summary**

When tapping on any event card within the \"My Upcoming Events\" or
\"Other Events\" sections, the application crashed, displaying a red
screen with the following error:

Uncaught Error: Property \'handleEventPress\' doesn\'t exist.

The crash occurred because the renderEventCard function in the Events
component was attempting to fire an onPress handler (handleEventPress)
that had not been defined.

**Files Involved**

- **Component File:** Events.tsx (The main screen rendering the event
  lists)

- **Constants File:** src/constants/navigation.ts (Contains the
  SCREEN_NAMES definitions)

**Important Code Snippets & Solution**

**1. The Trigger (in Events.tsx)**

Inside the renderEventCard function, the TouchableOpacity was calling
the undefined function:

TypeScript

\<TouchableOpacity

style={styles.eventCard}

onPress={() =\> handleEventPress(item)} // This line triggered the crash

activeOpacity={0.7}

\>

**2. The Navigation Constants (in src/constants/navigation.ts)**

We needed to verify the correct route name for the event details page to
write the navigation logic:

TypeScript

export const SCREEN_NAMES = {

// \... other screens

EVENTS: \'Events\',

EVENT_DETAILS: \'EventDetails\', // The target destination

// \...

} as const;

**3. The Solution (Added to Events.tsx)**

To resolve the error, we defined the missing handleEventPress function
inside the main Events component using useCallback. This successfully
catches the tap event and navigates the user to the EventDetails screen,
passing the relevant eventId as a parameter.

TypeScript

const handleEventPress = useCallback((event: Event) =\> {

navigation.navigate(SCREEN_NAMES.EVENT_DETAILS as any, {

eventId: event.id

});

}, \[navigation\]);

*(Note: This block was placed alongside the other component handlers,
right below handleCreateEvent).*

# Problem 54

**REDUCING THE SPACE BETWEEN TRENDING IN FEED AND IT'S ABOVE ELEMENT IN
HOME SCREEN**\
You've successfully tightened the layout between the **HomeHeader** and
the **Trending Feed** by addressing spacing at three different levels:
the layout wrapper, the shared component, and the specific
implementation.

Here is the summary of the changes you've implemented for your records:

## **1. SectionHeader.tsx (Shared Component)**

**Objective:** Enable style overrides so specific sections can be
adjusted without affecting the entire app.

- **Interface Update:** Added titleStyle?: object to SectionHeaderProps.

- **Implementation:** Applied the titleStyle prop to the Text component
  alongside the default styles.title.

TypeScript

// Updated SectionHeader.tsx

const SectionHeader = ({

title,

onViewAll,

containerStyle,

titleStyle // Added prop

}: SectionHeaderProps) =\> {

return (

\<View style={\[styles.container, containerStyle\]}\>

\<Text style={\[styles.title, titleStyle\]}\>{title}\</Text\>

{/\* \... \*/}

\</View\>

);

};

## **2. homeStyles.ts (Global Layout Styles)**

**Objective:** Remove the external \"buffer\" space added by the
screen-level container.

- **Change:** Modified the fullScrollViewContainer to remove the default
  theme spacing.

TypeScript

// Updated homeStyles.ts

fullScrollViewContainer: {

alignItems: \'stretch\',

marginTop: 0, // Reduced from theme.spacing.sm

paddingHorizontal: theme.spacing.xs,

},

## **3. TrendingFeed.tsx (Component Implementation)**

**Objective:** Perform the final \"micro-adjustment\" to bring the
content flush with the header.

- **Change:** Used the new override props to eliminate the internal
  title margin and used a negative margin to counteract the padding from
  the component above (HomeHeader).

TypeScript

// Updated TrendingFeed.tsx

return (

\<View style={styles.container}\>

\<SectionHeader

title={t(\'homeComponents.trendingFeed\')}

// Pulls the entire component upward to overlap the Header\'s bottom
padding

containerStyle={{ marginTop: -8 }}

// Removes the default md margin-top internal to the title text

titleStyle={{ marginTop: 0 }}

/\>

{/\* \... mapping logic \*/}

\</View\>

);

## **Why this approach works:**

1.  **Non-Destructive:** By adding props to SectionHeader instead of
    changing its stylesheet, you ensured other screens (like Communities
    or Events) stayed exactly the same.

2.  **Layered Control:** You removed the container margin first, then
    the text margin, and finally used the negative margin to \"reach
    into\" the HomeHeader\'s padding zone.

# Problem 55

AI Chatbot -- Input Field Shifting When Searching or Opening Keyboard

In the AI Chatbot interface, the input field shifts its position
whenever a search is performed or when the keyboard opens for typing.
This causes layout instability and affects the typing experience.

After typing in the search bar when keyboard is closed, the Input Fields
shifts above. check the screenshot for reference.

You need to make modifications in exactly **two places** in your file.

## **Modification 1: The KeyboardAvoidingView Props**

Scroll down to roughly **Line 468**.

**Change this: in src/screens/chat_bot/ChatBotScreen.tsx**

TypeScript

\<KeyboardAvoidingView

style={{ flex: 1, backgroundColor: \'transparent\' }}

contentContainerStyle={{ flexGrow: 1 }}

behavior={Platform.OS === \'ios\' ? \'padding\' : \'height\'}

keyboardVerticalOffset={Platform.OS === \'ios\' ? 0 : 45}

\>

**To this:**

TypeScript

\<KeyboardAvoidingView

style={{ flex: 1, backgroundColor: \'transparent\' }}

contentContainerStyle={{ flexGrow: 1 }}

behavior={Platform.OS === \'ios\' ? \'padding\' : \'padding\'}

keyboardVerticalOffset={0}

\>

*(Changing behavior to \'padding\' and removing the 45 offset stops
Android from double-lifting the input).*

## **Modification 2: The inputContainer Padding**

Scroll down to your styles, roughly **Line 810**.

**Change this:**

TypeScript

inputContainer: {

flexDirection: \'row\',

padding: theme.spacing?.md,

paddingBottom: (insets.bottom \|\| theme.spacing?.md) +
(theme.spacing?.xs \|\| 0),

backgroundColor: theme.isDark ? \'#1A1A1A\' : \'#FAFAFA\',

alignItems: \'flex-end\',

gap: 12,

},

**To this:**

TypeScript

inputContainer: {

flexDirection: \'row\',

padding: theme.spacing?.md,

paddingBottom: insets.bottom \|\| theme.spacing?.md,

backgroundColor: theme.isDark ? \'#1A1A1A\' : \'#FAFAFA\',

alignItems: \'flex-end\',

gap: 12,

},

*(Removing the extra math prevents the padding from jumping when Android
recalibrates the bottom safe area inset after the keyboard opens).*

# Problem 56

**Centering the title which is on the right of the back button**

To perfectly center the title across all screens (regardless of whether
there is a back button on the left or an icon on the right), you need to
separate the title from the left container and use **absolute
positioning**.

Here are the exactly two modifications you need to make in
src/components/common/TopHeader.tsx.

## **Modification 1: Update the JSX Structure**

Scroll to the return statement and move the titleContainer *outside* of
the left container so it sits in the middle.

**Replace your current return block with this:**

TypeScript

return (

\<View style={styles.topContainer}\>

{/\* 1. Left Side (Back Button) \*/}

\<View

style={\[

styles.container,

!showBackButton && {

padding: theme.spacing.md,

},

\]}

\>

{showBackButton && (

\<IconButton

icon=\"arrow-left\"

onPress={() =\> {

if (\_onBackPress) {

\_onBackPress();

} else {

navigation.goBack();

}

}}

iconColor={theme.colors.text}

/\>

)}

\</View\>

{/\* 2. Dead-Center Title (Absolutely Positioned) \*/}

\<View style={styles.titleContainer} pointerEvents=\"none\"\>

{showTitle && (

\<Text style={styles.title} numberOfLines={1} ellipsizeMode=\"tail\"\>

{title}

\</Text\>

)}

{subTitle && (

\<Text style={styles.subTitle} numberOfLines={1}
ellipsizeMode=\"tail\"\>

{subTitle}

\</Text\>

)}

\</View\>

{/\* 3. Right Side Component \*/}

\<View style={styles.rightContainer}\>

{rightComponent}

\</View\>

\</View\>

);

## **Modification 2: Update the Styles**

Scroll down to your headerStyles. We need to make the header relative
and the title container absolute so it ignores the width of the side
buttons.

**Update these specific styles:**

JavaScript

topContainer: {

justifyContent: \'space-between\',

flexDirection: \'row\',

alignItems: \'center\',

width: \'100%\',

backgroundColor: theme.isDark ? \'#1A1A1A\' : \'#FAFAFA\',

position: \'relative\', // \<\-- Add this

minHeight: 56, // \<\-- Add this so the header keeps its height

},

container: {

flexDirection: \'row\',

alignItems: \'center\',

zIndex: 1, // \<\-- Add this so the button remains clickable

},

rightContainer: {

zIndex: 1, // \<\-- Add this for the right component

},

titleContainer: {

position: \'absolute\', // \<\-- Change to absolute

left: 0, // \<\-- Stretch across the whole screen

right: 0,

top: 0,

bottom: 0,

justifyContent: \'center\',

alignItems: \'center\',

zIndex: 0,

},

*(Note: Adding pointerEvents=\"none\" to the JSX and managing the zIndex
guarantees that your centered title will never accidentally block the
user from clicking the back button, even on smaller screens!)*

# Problem 57

Here is a complete summary of the issue and the solution for your future
reference.

## **The Problem**

When a user logs out of the app, their access token is immediately
deleted. However, lingering background API requests or React Query
refetches attempt to fire without that token. The global Axios response
interceptor catches these failures and blindly triggers a red \"Access
token required\" toast message, disrupting what should be a seamless
logout experience.

## **The Solution**

The fix requires a two-step approach to safely shut down background
requests and suppress the specific error message during the logout
cycle.

## **1. Clear React Query Cache on Logout**

**File:** SettingsScreen.tsx (or wherever your Settings screen is
located)

**Action:** Stop React Query from attempting any background fetches the
moment the user taps \"Logout\".

**Code Snippet:**

JavaScript

// 1. Add the import at the top of the file

import { queryUtils } from \'@/api/queryClient\';

// 2. Modify the Primary Logout Button\'s onPress handler

\<TouchableOpacity

style={styles.logoutPrimaryButton}

onPress={() =\> {

queryUtils.clear(); // \<\-- Kills pending/background queries

logout();

hideDialog();

}}

\>

\<Text style={styles.logoutPrimaryButtonText}\>Logout\</Text\>

\</TouchableOpacity\>

## **2. Suppress the Toast in the API Interceptor**

**File:** src/api/config.ts

**Action:** Tell the global Axios error handler to display all error
toasts *except* when the error is specifically complaining about a
missing access token.

**Code Snippet:**

Find the error handler inside apiClient.interceptors.response.use (near
the bottom of the file) and update the toast.error line.

**Before:**

JavaScript

toast.error(error.response?.data?.message \|\| error.message \|\|
\'Something went wrong\');

**After:**

JavaScript

const errorMessage = error.response?.data?.message \|\| error.message
\|\| \'Something went wrong\';

// Silently ignore the missing token error so it doesn\'t pop up on
logout

if (errorMessage !== \'Access token required\') {

toast.error(errorMessage);

}

# Problem 58

After creating a question it now send the user to community-\>questions
tab where the user can see his latest questions once he refreshes the
tab

File: src/screens/community/CreateQuestion.tsx

React Navigation is throwing this error because CommunityDashboard is
hidden inside your Bottom Tab Navigator (MainTabParamList). Since
CreateQuestionScreen is a full-screen modal/stack on top of everything
(RootStackParamList), it cannot \"see\" the screens inside the bottom
tabs directly.

## **Option 1: The Easiest Fix (Highly Recommended)**

Since you likely pressed the \"New Post\" button *from* the Activities
feed to get to this screen, the safest and most standard way to return
to that feed is simply to go back to the previous screen in the stack:

TypeScript

const onSubmit = (data: any) =\> {

const payload = {

title: data?.question,

};

handleQuestionCreationMutate(payload, {

onSuccess: () =\> {

reset();

// Just go back to the feed you came from!

if (navigation.canGoBack()) {

navigation.goBack();

}

},

});

};

# Problem 59

Here is a quick summary of the prop-based customization you implemented.
This is a highly reusable pattern for styling shared components in React
Native.

## **What You Did**

You applied screen-specific Figma styles to a globally shared component
(HashtagSelector) by injecting optional style props. This allows
CreateQuestionScreen to have custom chips while ensuring all other
screens gracefully fall back to the default styles.

## **1. The Shared Component: HashtagSelector.tsx**

You updated the interface to accept optional style overrides and merged
them into the existing style arrays using \[defaultStyle,
optionalPropStyle\].

**Important Snippets:**

TypeScript

// 1. Added optional style props to the Interface

interface HashtagSelectorProps {

// \... existing props

unselectedChipStyle?: any;

selectedChipStyle?: any;

unselectedTextStyle?: any;

selectedTextStyle?: any;

labelStyle?: any;

}

// 2. Merged props into the styles arrays inside the component

\<TouchableOpacity

style={\[

styles.addTagButton,

unselectedChipStyle, // Injected here

error && styles.displayContainerError

\]}

\>

\<Text style={\[styles.addTagText, unselectedTextStyle\]}\>+
New\</Text\>

\</TouchableOpacity\>

## **2. The Implementation Screen: CreateQuestionScreen.tsx**

You defined the custom Light/Dark mode styles at the bottom of the file
and passed them directly into the updated \<HashtagSelector /\>.

**Important Snippets:**

TypeScript

// 1. Passing the custom styles as props

\<HashtagSelector

control={control}

name=\"tags\"

label=\"Add #Tag\"

labelStyle={{ textTransform: \'none\' }} // Overrides default uppercase

unselectedChipStyle={styles.unselectedChip}

selectedChipStyle={styles.selectedChip}

unselectedTextStyle={styles.unselectedText}

selectedTextStyle={styles.selectedText}

/\>

// 2. Defining the Light/Dark mode styles inside createStyles

unselectedChip: {

borderWidth: 1,

borderColor: theme.isDark ? \'#333333\' : \'#E5E5E5\',

backgroundColor: \'transparent\',

},

selectedChip: {

borderWidth: 1,

borderColor: \'#FF6B0033\',

backgroundColor: \'transparent\',

},

// \... corresponding text styles

Would you like to explore setting up any other shared components using
this pattern?

# Problem 60

When the user input/text field was empty in community-\>feed-\>click on
a card/post

## **Problem**

The goal was to visually indicate when a user cannot submit a comment by
fading out the \"send\" icon and disabling it whenever the text input
field is empty (or contains only whitespace).

## **Files Modified**

- **Target File:**
  src/screens/community/components/common/CommentInput.tsx

- *(Note: No changes were needed in PostDetail.tsx because
  component-specific UI logic should be encapsulated within the
  component itself for reusability and clean architecture).*

## **Code Snippets**

#### **Before**

The useForm hook didn\'t track the live value of the input, and the
IconButton was always fully visible and enabled.

TypeScript

// 1. Hook initialization

const { control, handleSubmit, reset } = useForm\<{ text: string }\>({

defaultValues: { text: \'\' },

});

// \...

// 2. Icon Button

\<IconButton

icon=\"send\"

onPress={handleSubmit(submit)}

loading={submitting}

iconColor={theme.colors.primary}

style={styles.button}

/\>

#### **After**

The watch function was added to monitor the input, and its value was
used to conditionally apply a disabled state and an opacity style to the
button.

TypeScript

// 1. Hook initialization (added \'watch\')

const { control, handleSubmit, reset, watch } = useForm\<{ text: string
}\>({

defaultValues: { text: \'\' },

});

// 2. Track the text value

const textValue = watch(\'text\');

// \...

// 3. Icon Button (added \'disabled\' and dynamic \'opacity\')

\<IconButton

icon=\"send\"

onPress={handleSubmit(submit)}

loading={submitting}

iconColor={theme.colors.primary}

disabled={!textValue \|\| textValue.trim() === \'\'}

style={\[

styles.button,

{ opacity: textValue && textValue.trim() !== \'\' ? 1 : 0.4 }

\]}

/\>

## **Solution & Key Takeaways**

1.  **Live State Monitoring:** By extracting watch from react-hook-form,
    the component can constantly monitor the text field\'s current value
    without requiring a separate useState hook.

2.  **Conditional Styling & Props:** The textValue is checked to see if
    it is empty or just spaces (!textValue \|\| textValue.trim() ===
    \'\'). If it is empty, the IconButton receives disabled={true} and
    an inline style of opacity: 0.4 to create the faded look.

3.  **Encapsulation:** By making these changes directly inside
    CommentInput.tsx, any screen that imports this component (like your
    PostDetail screen) will automatically inherit this behavior, keeping
    your codebase modular and D.R.Y. (Don\'t Repeat Yourself).

# Problem 61

community-\>feed-\>any card/post

## **Problem**

When a user successfully posted a new comment, the app triggered a
background refetch of the comments list to display the new entry.
However, the orange refresh icon next to \"All Comments\" was tied to
React Query\'s global isFetching state. This caused the icon to spin
every time a background update occurred, creating a jarring user
experience since the user didn\'t manually request the refresh.

## **Files Modified**

- **Target File:**
  src/screens/community/components/common/CommentSection.tsx

## **Code Snippets**

#### **Before**

The TouchableHighlight used the global isFetching state directly from
the useListComments hook.

TypeScript

// 1. Hook initialization

const { data, refetch, isFetching } = useListComments(postId);

// \...

// 2. Refresh Icon UI

\<TouchableHighlight onPress={() =\> refetch()}
underlayColor={theme.colors.surface}\>

{isFetching ? (

\<ActivityIndicator size={20} /\>

) : (

\<Icon source=\"refresh\" size={20} color={theme.colors.primary} /\>

)}

\</TouchableHighlight\>

#### **After**

The global isFetching state was removed. Instead, a local state
(isManualRefreshing) and a dedicated click handler were added to isolate
the spinning animation to manual user taps only.

TypeScript

// 1. Hook initialization (removed isFetching)

const { data, refetch } = useListComments(postId);

// 2. Add local state and handler

const \[isManualRefreshing, setIsManualRefreshing\] =
React.useState(false);

const handleRefreshClick = React.useCallback(async () =\> {

setIsManualRefreshing(true);

try {

await refetch();

} finally {

setIsManualRefreshing(false);

}

}, \[refetch\]);

// \...

// 3. Refresh Icon UI (using local state and custom handler)

\<TouchableHighlight onPress={handleRefreshClick}
underlayColor={theme.colors.surface}\>

{isManualRefreshing ? (

\<ActivityIndicator size={20} /\>

) : (

\<Icon source=\"refresh\" size={20} color={theme.colors.primary} /\>

)}

\</TouchableHighlight\>

Modifying CommentSection.tsx directly is exactly the right move for the
exact reason you mentioned: **reusability**.

Here is why this approach is the industry standard:

- **App-Wide Consistency:** Because CommentSection handles its own
  loading state now, anywhere you import this component (whether it\'s
  on a text post, a photo detail screen, or an article page), it will
  behave perfectly. You won\'t have to remember to rewrite that
  isManualRefreshing logic on every single screen.

- **Easier Maintenance:** If your design team decides to change that
  orange refresh icon to a different color or shape next month, you only
  have to update it in this one file, and the whole app updates
  instantly.

- **Clean Parent Components:** Screens like PostDetail are already busy
  handling the keyboard, the main post data, and navigation. By making
  CommentSection self-sufficient, you keep the parent screen\'s code
  clean and focused only on the big picture.

## **Solution & Key Takeaways**

1.  **Decoupling Background vs. Manual Fetching:** React Query\'s
    isFetching is true whenever data is being fetched, regardless of
    what triggered it (a manual click, a window focus, or a mutation
    success). By decoupling the UI spinner from this global state, you
    prevent unintended animations during silent background updates.

2.  **Local State for User Intent:** Implementing isManualRefreshing
    ensures that the visual loading indicator strictly responds to
    direct user intent (tapping the icon).

3.  **Seamless UX:** When a comment is now added,
    queryClient.refetchQueries still updates the list seamlessly in the
    background, but the user is no longer distracted by the spinning
    icon, resulting in a much cleaner and professional feel.

# Problem 62

In Chats-\>any chat tab

![](data/media_dump/media/image10.png){width="1.6716316710411199in"
height="3.6718755468066493in"}

Here is a complete summary of the keyboard overlap issue, the root
cause, the solution, and best practices to keep in your engineering
notes for future reference.

**File: src/screens/chat/ChatRoomScreen.tsx**

## **Problem Statement**

In the chat interface, the text input field was completely hidden behind
the on-screen keyboard when a user attempted to type a message on
Android devices. This occurred despite using React Native\'s standard
KeyboardAvoidingView, forcing users to constantly close the keyboard to
see what they were typing.

## **The Root Cause**

The core issue was a conflict between Android\'s native window
management and React Native\'s layout engine:

1.  **Translucent Status Bar:** The application utilizes a
    \<CustomStatusBar translucent={true} /\>. This creates an
    \"edge-to-edge\" UI layout.

2.  **Native Override:** When a translucent status bar is active on
    Android, it overrides and disables the
    android:windowSoftInputMode=\"adjustResize\" setting in the
    AndroidManifest.xml.

3.  **KeyboardAvoidingView Failure:** Because the native Android window
    was no longer resizing itself, React Native\'s KeyboardAvoidingView
    could not accurately calculate the screen dimensions or the
    keyboard\'s intrusion, causing the behavior=\"padding\" prop to
    silently fail.

## **The Solution**

To guarantee consistent behavior across all screen sizes, the solution
bypasses KeyboardAvoidingView\'s automatic Android calculations.
Instead, it listens directly to the native OS for the exact keyboard
height and manually applies that exact pixel value as bottom padding to
the main container. iOS is left to use its reliable native padding
behavior.

## **Important Code Snippets**

**1. The Keyboard Listener Hook**

Capture the exact keyboard height dynamically when it opens, and reset
it when it closes.

TypeScript

**//src/screens/chat/ChatRoomScreen.tsx**

import { Keyboard, Platform } from \'react-native\';

import React, { useState, useEffect } from \'react\';

// Inside your component:

const \[keyboardPadding, setKeyboardPadding\] = useState(0);

useEffect(() =\> {

const showSubscription = Keyboard.addListener(

Platform.OS === \'ios\' ? \'keyboardWillShow\' : \'keyboardDidShow\',

\(e\) =\> {

// Only apply manual padding on Android

if (Platform.OS === \'android\') {

setKeyboardPadding(e.endCoordinates.height);

}

}

);

const hideSubscription = Keyboard.addListener(

Platform.OS === \'ios\' ? \'keyboardWillHide\' : \'keyboardDidHide\',

() =\> {

if (Platform.OS === \'android\') {

setKeyboardPadding(0);

}

}

);

return () =\> {

showSubscription.remove();

hideSubscription.remove();

};

}, \[\]);

**2. The Dynamic Container Implementation**

Apply the calculated height to the container while preventing conflicts
with the default iOS behavior.

TypeScript

\<KeyboardAvoidingView

style={\[

styles.container,

{ paddingBottom: keyboardPadding } // Dynamically inject the exact
keyboard height

\]}

behavior={Platform.OS === \'ios\' ? \'padding\' : undefined} // Let iOS
handle itself

keyboardVerticalOffset={Platform.OS === \'ios\' ? 0 : 0}

\>

{/\* Your Chat UI Components \*/}

\</KeyboardAvoidingView\>

## **Best Practices for Future Reference**

- **Avoid Hardcoded Pixel Values:** Never hardcode padding (e.g.,
  paddingBottom: 300) to fix keyboard issues. Android device screens and
  keyboard apps (Gboard, SwiftKey) vary drastically in height. Always
  use e.endCoordinates.height to calculate the exact footprint
  dynamically.

- **Isolate Platform Logic:** iOS and Android handle UI rendering
  completely differently. Use Platform.OS checks to ensure fixes applied
  to Android don\'t accidentally break perfectly functioning iOS
  features.

- **Audit Native UI Dependencies:** Whenever a standard React Native
  layout component (like KeyboardAvoidingView or SafeAreaView) fails,
  always check if a native UI element (like a translucent Status Bar or
  Navigation Bar) is altering the device\'s default rendering behavior.

- **Log Event Payloads:** When debugging device hardware events, logging
  the event object (like e.nativeEvent.layout or e.endCoordinates) is
  the fastest way to verify if React Native is actually receiving the
  correct data from the mobile OS.

# Problem 63

Here is a concise summary of the task, the solution, and the
architectural best practices we used to keep your codebase clean and
safe.

## **📋 The Problem**

The **Gender** field in the profile edit screen was using a full-screen,
searchable interface. For a field with only three options (**Male**,
**Female**, **Prefer not to say**), a search bar is unnecessary and
creates friction. The goal was to convert it into a **bottom-sheet style
dropdown** without breaking the searchable functionality on other
screens (like **Location**).

## **🛠️ Code Files & Snippets**

## **1. src/components/forms/AutocompleteField.tsx (The Shared Component)**

We modified the shared component to be \"prop-aware.\" It now checks if
it *should* be searchable. If not, it transforms the UI into a bottom
sheet.

- **Logic Change:** Added a check for config.searchable !== false.

- **UI Change:** Updated the Modal props to support transparency and
  added a conditional container for the bottom-sheet effect.

TypeScript

\<Modal

visible={modalVisible}

transparent={config.searchable === false} // Overlays instead of
replacing the screen

presentationStyle={config.searchable === false ? \'overFullScreen\' :
\'fullScreen\'}

\>

\<SafeAreaView style={\[styles.modalSafeArea, config.searchable ===
false && styles.modalOverlay\]}\>

\<View style={config.searchable === false ?
styles.dropdownModalContainer : { flex: 1 }}\>

{/\* Header & List logic\... \*/}

\</View\>

\</SafeAreaView\>

\</Modal\>

## **2. src/screens/profile/components/BasicProfileEdit.tsx (The Screen)**

We configured the specific Gender field instance to \"opt-out\" of
searching and provided hardcoded options.

TypeScript

{

type: \'autocomplete\',

name: \'gender\',

label: \'Gender\',

options: \[

{ label: \'Male\', value: \'Male\' },

{ label: \'Female\', value: \'Female\' },

{ label: \'Prefer not to say\', value: \'Prefer not to say\' },

\],

searchable: false, // Disables the search bar and focuses the UI

searchType: \'custom\', // Skips unnecessary API calls

}

## **✅ The Solution**

By using a **conditional prop logic** (searchable), we achieved a
dual-purpose component:

1.  **Search Mode (Default):** Used for large datasets (Locations,
    Companies). It remains a full-screen searchable list.

2.  **Dropdown Mode:** Triggered by passing searchable: false. It hides
    the search bar, prevents the keyboard from popping up, and slides up
    as a bottom sheet.

## **💡 Best Practices for Future Reference**

This is a great point to document. When working with shared UI
components like AutocompleteField, the \"Golden Rule\" of development
applies: **Never break the existing contract.**

Here is the technical summary and the \"correct way\" to handle shared
component modifications.

## **🚨 The Golden Rule: Shared Component Safety**

**The Problem:** If you directly modify AutocompleteField.tsx to hide
the search bar for \"Gender,\" you risk breaking every other screen in
the app (Location, Company, Skills) that relies on that search bar.

**The Correct Way:** Instead of hardcoding logic for one specific field,
you **add a new capability (a Prop)** to the shared component and give
it a **Default Value** that preserves the existing behavior. This
ensures \"Backward Compatibility.\"

# Problem 64

Here is a comprehensive, structured post-mortem and problem summary for
the **Recent Search History** feature implementation. You can save this
in your project documentation, Jira ticket, or Notion workspace for
future reference.

# **Implementation Report & Post-Mortem: Recent Search History Feature**

## **1. Feature Overview**

The objective was to implement a LinkedIn-style recent search history
feature. This involved fetching a user\'s prior search queries from the
backend and displaying them in a stylized list when the search bar was
empty, while showing a fallback empty state if no history existed. The
implementation strictly adhered to the \"Golden Rule\" of backward
compatibility, ensuring shared hooks and components remained untouched.

## **2. Phase 1: Architectural & Structural Fixes**

The initial implementation attempt encountered several critical UI and
logic errors that prevented the screen from rendering:

- **Recursive Rendering Loop:** The main Search screen used a FlatList
  to render its sections. Inside the renderTabContent function,
  individual category sections (PeopleSection, CompaniesSection, etc.)
  were also returning FlatLists. Nesting vertical FlatLists caused an
  infinite measurement loop and a white screen crash.

  - *Solution:* Refactored the internal section components to use
    standard View containers and .map() iterations instead of nested
    FlatLists.

- **Result Logic Deletion & Scope Errors:** Previous logic handling the
  display of actual search results was accidentally removed, and a
  syntax error (missing closing braces) broke the build.

  - *Solution:* Restored the scoped rendering logic for tabs and
    properly closed the component blocks.

- **Fragmented Section Logic:** The searchSections memoization was
  configured to completely hide the content section if no live search
  results were present. This inadvertently blocked the \"Recent
  Searches\" UI from ever mounting.

  - *Solution:* Updated the memoization logic to always render the
    content block, allowing renderTabContent to decide whether to show
    live results, recent history, or the empty state based on the input
    string length.

## **3. Phase 2: API Routing & Integration**

During the integration of the React Query hooks, the API calls failed
with a 404 Not Found error.

- **The Base URL Context:** The environment variables (API_BASE_URL)
  were verified to already include the /api/v1 suffix. Therefore, the
  endpoint path only needed to be /search/recent.

- **The Endpoint Typo:** Inside src/api/endpoints.ts, the SEARCH object
  had a typo where the key was lowercase and assigned to an array
  intended for React Query caching, causing Axios to evaluate the
  endpoint as undefined.

  - *Solution:* Corrected the endpoint definition to:

  - TypeScript

SEARCH: {

GLOBAL: \'/search\',

RECENT: \'/search/recent\',

}

- 
- 

## **4. Phase 3: Data Shape & React Rendering Crashes**

Once the API connected, the app immediately threw a Red Screen error:
*\"Objects are not valid as a React child\"*.

- **The Problem:** The frontend component was initially typed to expect
  a flat array of strings (string\[\]). However, the backend returned an
  array of objects (e.g., \[{ id: 1, query: \"tech\", type: \"global\",
  timestamp: \"\...\" }\]). React Native crashed when instructed to
  render the raw object inside a \<Text\> component.

- **The Solution:**

  1.  Updated the interface to accurately reflect the backend\'s data
      shape: interface RecentSearchItem { id?: number \| string; query:
      string; \... }.

  2.  Updated the JSX map function to explicitly render the string
      property: \<Text\>{item.query}\</Text\>.

## **5. Phase 4: Build System Quirks (The Phantom Crash)**

Even after fixing the data shape, the app continued to crash with the
exact same error.

- **The Problem:** The React Native Metro Bundler aggressively cached
  the broken version of the component file. Standard terminal commands
  (\--reset-cache) failed to bust this specific file cache, meaning the
  app was ignoring the newly saved code.

- **The Solution (Cache-Busting):** Renamed the component file from
  RecentSearchesList.tsx to RecentSearchHistory.tsx and updated the
  import path in Search.tsx. This forced the bundler to treat it as a
  brand-new file, bypassing the cache and instantly resolving the crash.

## **6. Phase 5: UI Refinements & Pending Backend Action**

With the list successfully rendering, two final polish items were
addressed:

- **UI Overflow (Frontend Fix):** To prevent the recent searches list
  from taking up the entire screen if the user had hundreds of history
  items, a hard limit was applied on the UI side.

  - *Solution:* Chained a .slice(0, 5) method before the .map() function
    in RecentSearchHistory.tsx to strictly cap the displayed items to 5.

- **Duplicate Entries (Backend Action Required):** The API currently
  returns duplicate search terms (e.g., the word \"tech\" appeared
  multiple times in a row).

  - *Pending Action:* The backend team needs to implement grouping on
    their end (e.g., using SELECT DISTINCT or a similar GROUP BY SQL
    clause) so the API only returns unique search queries to the
    frontend.

**2. Required Files**

The following files are necessary for the complete end-to-end
integration:

  -------------------------------------------------------------------------------------------
  **File          **File Path**                                     **Purpose**
  Category**                                                        
  --------------- ------------------------------------------------- -------------------------
  **Constants**   src/api/endpoints.ts                              Define the
                                                                    /api/v1/search/recent
                                                                    path.

  **Constants**   src/api/queryKeys.ts                              Define a unique queryKey
                                                                    for caching history data.

  **Service**     src/api/services/search.service.ts                Implement the
                                                                    getRecentSearches API
                                                                    call using apiClient.

  **Hook**        src/api/hooks/useSearch.ts                        Create the
                                                                    useGetRecentSearches hook
                                                                    using
                                                                    \@tanstack/react-query.

  **UI            src/screens/search/RecentSearchHistory.tsx        Render the list of
  Component**                                                       history items with icons
                                                                    and labels.

  **UI            src/screens/search/RecentSearchesEmptyState.tsx   Render the fallback UI
  Component**                                                       when no search history is
                                                                    found.

  **Main Screen** src/screens/search/Search.tsx                     Orchestrate the logic
                                                                    between history, loading
                                                                    states, and results.
  -------------------------------------------------------------------------------------------

**3. Identified Problems (Previous Attempt)**

The previous code iteration failed due to several critical architectural
and syntax errors:

- **Recursive Rendering Loop:** You attempted to render the main
  screen\'s FlatList *inside* the renderTabContent function. Because
  renderTabContent is called by renderItem, which is inside the
  FlatList, it created an infinite rendering loop that would crash the
  app.

- **Result Logic Deletion:** The logic required to render the
  PeopleSection, CompaniesSection, CommunitiesSection, and JobsSection
  was accidentally removed. This meant that even after a user typed a
  query, no results would be displayed.

- **Syntax & Scope Errors:** The Search component function was not
  properly closed with braces before the export default statement,
  leading to a \"Unexpected token\" build error.

- **Fragmented Section Logic:** The searchSections memoization was
  configured to hide the content section if no search results were
  present. This blocked the \"Recent Searches\" list from ever
  appearing, as the container it lived in was being conditionally
  removed.

.env file has something like
API_BASE_URL=https://your-server.com/api/v1, then your Step 1 code
(RECENT: \'/search/recent\')

**One quick observation:** Looking at your screenshot, the backend is
returning duplicate searches for \"tech\" over and over. You might want
to let your backend team know so they can group the results (using
SELECT DISTINCT or similar on their end) so the user only sees unique
search terms!

# Problem 65

Here is a summary of the issue, root cause, and the solution for your
future reference:

## **Issue Summary: \"Invalid Profile ID Provided\" Error**

**The Problem:**

When clicking the user avatar on the Home screen to navigate to the \"My
Profile\" page, a toast error message stating \"Invalid profile id
provided\" would appear.

**The Root Cause:**

The issue was a frontend React Query behavior triggering a backend
validation error.

When navigating to \"My Profile\", no userId is passed in the navigation
parameters (which is the correct behavior). However, the Profile.tsx
screen unconditionally calls two hooks on mount:

1.  useGetUserProfile (to fetch your own data)

2.  useGetOtherUserProfile (to fetch another user\'s data)

Because useGetOtherUserProfile did not check if a userId actually
existed before running, it immediately fired an API request with an
undefined ID. The backend caught this invalid request and threw the
error toast.

**Files Involved:**

- src/components/home/HomeHeader.tsx (Navigation trigger)

- src/screens/profile/Profile.tsx (Where the hooks were called)

- src/api/hooks/useProfile.ts (Where the hook logic was defined)

Here is the original code snippet from src/api/hooks/useProfile.ts that
was causing the error:

TypeScript

// Previous code that caused the error

export const useGetOtherUserProfile = (userId: string \| number) =\> {

const { isAuthenticated } = useAuthStore();

return useQuery({

queryKey: \[queryKeys.profile.getOtherUserProfile, userId\],

queryFn: () =\> getOtherUserProfile(userId),

enabled: isAuthenticated, // \<\-- Missing the check for a valid userId

});

};

In this version, userId was strictly typed (not optional), and the
enabled property only checked if the user was authenticated. This
allowed the query to run immediately on the \"My Profile\" page even
when userId was undefined, triggering the backend error.

## **The Solution**

The fix involved updating the useGetOtherUserProfile hook in
src/api/hooks/useProfile.ts to make the userId optional and adding an
enabled condition to ensure the API call *only* fires when a valid
userId is present.

**Code Snippet (src/api/hooks/useProfile.ts):**

TypeScript

// Updated useGetOtherUserProfile hook

export const useGetOtherUserProfile = (userId?: string \| number) =\> {
// 1. Made userId optional

const { isAuthenticated } = useAuthStore();

return useQuery({

queryKey: \[queryKeys.profile.getOtherUserProfile, userId\],

// 2. Type cast to prevent TypeScript errors since execution is blocked
if undefined

queryFn: () =\> getOtherUserProfile(userId as string \| number),

// 3. ADDED: !!userId ensures this hook never fires an API request if
there is no ID

enabled: isAuthenticated && !!userId,

});

};

# Problem 66

Here is a clean summary of the issue and the fix for your documentation.

## **Bug Summary: 400 Bad Request on Profile Update**

**The Issue**

When updating the user profile, selecting a dropdown option (like Gender
or Location) triggered a 400 Bad Request API error with the message:
\"genderId must be a number\" (or locationId must be a number).

This happened because the handleFormSubmit function was blindly forcing
string values (e.g., \'Male\') into numbers using Number(), which
evaluates to NaN (Not-a-Number). During the JSON stringification process
for the API request, NaN is converted to null. The backend\'s strict
validation rejected the null value, expecting either a valid number or
for the field to be completely omitted.

**File Modified**

- src/screens/profile/components/BasicProfileEdit.tsx

## **The Old Code (Error Causing)**

The direct cast to Number() caused the NaN to null conversion in the
payload.

TypeScript

const payload = {

displayName: data.displayName,

titleLine: data.titleLine,

avatarUrl: data.avatarUrl ?? undefined,

// ❌ Fails when value is a string like \"Male\", returning NaN -\> null

locationId: data.location?.value ? Number(data.location.value) :
undefined,

genderId: data.gender?.value ? Number(data.gender.value) : undefined,

genderName: typeof data.gender?.label === \'string\' ? data.gender.label
: undefined,

};

## **The Solution**

We parsed the numbers first and added a !Number.isNaN() check. If the
parsed result is NaN, it safely falls back to undefined, which
completely strips the key from the JSON payload, preventing the explicit
null submission and allowing the backend to accept the request.

TypeScript

const parsedLocationId = data.location?.value ?
Number(data.location.value) : undefined;

const parsedGenderId = data.gender?.value ? Number(data.gender.value) :
undefined;

const payload = {

displayName: data.displayName,

titleLine: data.titleLine,

avatarUrl: data.avatarUrl ?? undefined,

// ✅ Only attaches the ID if it successfully parses into an actual
number

locationId: !Number.isNaN(parsedLocationId) ? parsedLocationId :
undefined,

genderId: !Number.isNaN(parsedGenderId) ? parsedGenderId : undefined,

genderName: typeof data.gender?.label === \'string\' ? data.gender.label
: undefined,

};

# Problem 67

## **The Problem**

- **Symptoms:** Clicking a \"Trending Today\" chip (like *Funding* or
  *Discussion*) updated the selected state, but no posts appeared below
  it. Furthermore, clicking the chip a second time failed to deselect
  it, essentially freezing the chip\'s UI state.

- **The Error:** A RedBox error was thrown stating: Property
  \'navigation\' doesn\'t exist.

- **Root Cause:** There were two underlying issues in the
  TopicDiscussions component:

  1.  **Hidden UI:** The JSX code responsible for actually mapping and
      rendering the PostCard components was commented out.

  2.  **Missing Navigation Hook:** Once the code was uncommented, the
      PostCard component tried to execute navigation.navigate when a
      post was clicked. However, navigation was never initialized inside
      the TopicDiscussions wrapper. This caused an unhandled JS
      exception that crashed the component tree, preventing React from
      re-rendering the screen to show the posts or process the
      deselection clicks.

## **Files Involved**

- src/screens/community/components/community-dashboard/TabScreen/components/TrendingTopics.tsx

## **The Code Changes**

#### **Before (The Broken State)**

The data extraction and rendering logic was commented out, and
navigation was missing.

TypeScript

const TopicDiscussions: React.FC\<{ slug: string }\> = React.memo(({
slug }) =\> {

const theme = useTheme();

useDisucssionByTrendingTopic(slug);

// const discussions = data?.data?.items ?? \[\];

return (

\<View style={{ marginBottom: 12 }}\>

\<Text style={{ fontSize: 16, fontWeight: \'600\', color:
theme.colors.text, marginBottom: 4 }}\>

{slug.toUpperCase()} Discussions

\</Text\>

{/\* {isFetching && \<ActivityIndicator color={theme.colors.primary}
size=\"small\" /\>}

// \... (rest of the rendering logic was commented out)

\*/}

\</View\>

);

});

#### **After (The Fixed State)**

We imported useNavigation, initialized it inside the component,
uncommented the data extraction, and uncommented the UI rendering block.

TypeScript

// 1. Ensure this is imported at the top of the file

import { useNavigation } from \'@react-navigation/native\';

import { View, Text, StyleSheet, ActivityIndicator } from
\'react-native\';

import PostCard from \'../../../common/PostCard\';

// \...

const TopicDiscussions: React.FC\<{ slug: string }\> = React.memo(({
slug }) =\> {

const theme = useTheme();

// 2. Initialize navigation so PostCard doesn\'t crash

const navigation = useNavigation\<any\>();

// 3. Uncomment data extraction

const { data, isFetching, refetch } =
useDisucssionByTrendingTopic(slug);

const discussions = data?.data?.items ?? \[\];

return (

\<View style={{ marginBottom: 12 }}\>

\<Text style={{ fontSize: 16, fontWeight: \'600\', color:
theme.colors.text, marginBottom: 4 }}\>

{slug.toUpperCase()} Discussions

\</Text\>

{/\* 4. Uncomment the rendering block \*/}

{isFetching && \<ActivityIndicator color={theme.colors.primary}
size=\"small\" /\>}

{!isFetching && discussions.length === 0 && (

\<Text style={{ color: theme.colors.textSecondary }}\>No discussions
found for {slug}\</Text\>

)}

{!isFetching &&

discussions.map((d: any, idx: number) =\> (

\<PostCard

key={\`disc-\${slug}-\${idx}\`}

post={{

id: d.id,

title: d.title,

content: d.content,

user: {

userId: d.user_id,

name: \`User \${d.user_id}\`,

prefix: d.community_name ? \`c/\${d.community_name}\` :
\`u/\${d.user_id}\`,

avatar_url: \'https://picsum.photos/200\',

},

community: {

id: d.community_id,

name: d.community_name,

},

metrics: {

upvotes: parseInt(d.upvote_count \|\| \'0\', 10),

downvotes: 0,

comments: parseInt(d.comment_count \|\| \'0\', 10),

},

\...d,

}}

handlePostClick={() =\> {

// Navigation now works without throwing an error!

navigation.navigate(\'CommunityPostDetail\', { postId: d.id });

}}

refresh={refetch}

/\>

))}

\</View\>

);

});

## **The Takeaway**

When a piece of UI state (like a toggle or a chip) seems to \"freeze\"
or stop responding to clicks, it is almost always due to a silent
JavaScript error crashing that specific component\'s render cycle.
Checking the RedBox or console logs for missing variables (like
navigation) is the fastest way to unblock it.

# Problem 68

Here is a complete summary of the performance optimization regarding the
FlatList and API calls for your future reference.

## **The Problem**

- **Symptoms:** The app was experiencing unnecessary network strain and
  potential UI stuttering when scrolling through the community feed.

- **The Bottleneck:** The PostCard component was responsible for
  figuring out if the currently logged-in user authored the post (to
  determine whether to hide the \"Follow\" button). To do this, it
  called the useGetUserProfile() hook.

- **Root Cause:** Because PostCard is rendered inside a FlatList, it
  executes its hooks *per item*. If the screen rendered 15 posts, the
  app fired **15 simultaneous, identical API requests** to fetch the
  exact same user profile. As the user scrolled, it would continue
  firing redundant requests for every new post that appeared on screen.

## **Files Involved**

- src/screens/community/components/community-dashboard/TabScreen/components/TopDiscussions.tsx
  (The Parent)

- src/common/PostCard.tsx (The Child)

## **The Code Changes**

#### **Before (The Bottleneck State)**

The parent component just passed the post data, leaving every single
child component to fetch the profile independently.

**In TopDiscussions.tsx (Parent):**

TypeScript

const renderPost = React.useCallback(({ item }: { item: any }) =\> (

\<PostCard

post={item}

handlePostClick={\...}

refresh={refetch}

/\>

), \[\...\]);

**In PostCard.tsx (Child):**

TypeScript

// This fired an API call for EVERY post on the screen

const { data: userProfileData } = useGetUserProfile(undefined);

const UserUUID = pathOr(pathOr(\'\', \[\'user\', \'userId\'\], post),
\[\'user\', \'id\'\], post);

const isCurrentUser = pathOr(\'\', \[\'profile\', \'id\'\],
userProfileData) === UserUUID;

#### **After (The Optimized State)**

We hoisted the API call up to the parent component to fetch the profile
**once**. We then passed the user\'s ID down as an *optional* prop to
respect the Golden Rule of Backward Compatibility, ensuring we didn\'t
break PostCard on other screens that haven\'t been updated yet.

**In TopDiscussions.tsx (Parent):**

TypeScript

// 1. Fetch the profile ONCE at the top level

const { data: userProfileData } = useGetUserProfile(undefined);

const currentUserId = pathOr(\'\', \[\'profile\', \'id\'\],
userProfileData);

// 2. Pass it down to the child

const renderPost = React.useCallback(({ item }: { item: any }) =\> (

\<PostCard

post={item}

currentUserId={currentUserId} // Passed as a prop

handlePostClick={\...}

refresh={refetch}

/\>

), \[navigation, refetch, theme.spacing.md, currentUserId\]); // Added
to dependencies

**In PostCard.tsx (Child):**

TypeScript

// 1. Accept it as an OPTIONAL prop so old screens don\'t break

const PostCard = ({

post,

currentUserId,

// \...

}: {

currentUserId?: string;

// \...

})

// 2. Use the prop first, fallback to local fetch if it\'s missing

const UserUUID = pathOr(pathOr(\'\', \[\'user\', \'userId\'\], post),
\[\'user\', \'id\'\], post);

const fetchedUserId = pathOr(\'\', \[\'profile\', \'id\'\],
userProfileData);

// 3. The fallback logic

const isCurrentUser = (currentUserId \|\| fetchedUserId) === UserUUID;

## **The Takeaway**

When working with FlatList, **never put API calls inside the render
items** unless absolutely necessary. A list of 50 items will fire 50
requests. Always hoist your global/shared data fetches (like user
profiles, app settings, or theme data) to the parent screen and pass the
results down as props. Using optional props (currentUserId?) allows you
to optimize heavily used components incrementally without breaking the
rest of your app!

# Problem 69

## **The Problem**

The application experienced a fatal crash resulting in the error:
Objects are not valid as a React child (found: object with keys {label,
value}).

React Native requires children of \<Text\> components to be primitives
(strings or numbers). The crash occurred because the backend API was
returning certain profile fields (like positionName, companyName, or
employmentType) as a dropdown-style object {label: \"\...\", value:
\"\...\"} instead of a plain text string. When the UI attempted to map
and render these fields, the rendering engine threw an exception.

## **Affected Files**

- **Primary Culprit:** src/screens/profile/ExperienceTab.tsx

- **Proactive Fix:** src/screens/profile/components/UserProfileCard.tsx
  (or similar path)

## **The Code**

**The Old Code (Vulnerable)**

Variables were passed directly into the text component, assuming the API
would always return a string.

TypeScript

// Inside ExperienceTab.tsx

\<Text style={styles.experienceRole}\>

{pathOr(\'UserRole\', \[\'position\', \'positionName\'\], exp)}

\</Text\>

**The New Code (Safe)**

A helper function intercepts the data, checks its type, and forces it
into a string before React Native attempts to render it.

TypeScript

// 1. The Interceptor Function

const getSafeText = (val: any, fieldName: string): string =\> {

if (val === null \|\| val === undefined) return \'\';

if (typeof val === \'string\' \|\| typeof val === \'number\') return
String(val);

// Catches the rogue {label, value} object

if (typeof val === \'object\' && !Array.isArray(val)) {

console.warn(\`\[DEBUG\] Expected string for \${fieldName}, but got
object:\`, val);

if (\'label\' in val) return String(val.label);

if (\'value\' in val) return String(val.value);

}

return String(val);

};

// 2. The Implementation

\<Text style={styles.experienceRole}\>

{getSafeText(pathOr(\'UserRole\', \[\'position\', \'positionName\'\],
exp), \'positionName\')}

\</Text\>

## **The Solution**

The getSafeText function acts as a defensive layer. If the API returns
the correct string, it passes through untouched. If the API mistakenly
returns an object, the function safely extracts the .label or .value and
converts it to a string, entirely neutralizing the crash while logging a
warning for developers.

## **Best Practices to Avoid This**

1.  **Sanitize Form Submissions (The Root Cause):** This issue almost
    always originates on the frontend during data creation. When saving
    data from a dropdown or picker component, ensure your form logic
    extracts the actual string value before sending the POST/PUT
    request. Do not send the raw {label, value} state to your API.

2.  **Strict API Typing:** If you control the backend, enforce strict
    data validation on incoming requests to reject payloads where a
    string field receives a JSON object.

3.  **Defensive UI Architecture:** In React Native, dynamic text
    components should ideally be wrapped in a custom \<AppText\>
    component that automatically sanitizes its children, ensuring raw
    objects never reach the native rendering layer.

Note: there are 2 files named ExperienceTab.tsx

//69:

Here is a complete summary of the two UI and API alignment issues we
resolved, including the exact file changes and the architectural best
practices they highlight.

## **1. API Endpoint & Data Structure Update**

**The Problem:**

The backend endpoint for fetching \"Job Type\" options was updated. The
path changed from /autocomplete/employment-type to
/autocomplete/work-arrangement. Additionally, the JSON response schema
changed: the key used for the display text changed from type_name to
arrangement_type.

**The Solution:**

Instead of modifying the React UI components, we updated the central API
configuration and the specific service function responsible for
formatting this data. We used the nullish coalescing operator (??) to
check for the new arrangement_type key first, while keeping type_name as
a fallback.

**Files Modified:** \* src/endpoints.ts (or your constants file)

- src/services/autcomplete.service.ts

## **Code Snippets: src/endpoints.ts**

**Before:**

TypeScript

EMPLOYMENT_TYPE: (query: string) =\>
\`/autocomplete/employment-type?q=\${encodeURIComponent(query)}\`,

**After:**

TypeScript

EMPLOYMENT_TYPE: (query: string) =\>
\`/autocomplete/work-arrangement?q=\${encodeURIComponent(query)}\`,

## **Code Snippets: src/services/autcomplete.service.ts**

**Before:**

TypeScript

export const EmploymentType = async (query: string) =\> {

const response: any = await
apiClient.get(API_ENDPOINTS.AUTOCOMPLETE.EMPLOYMENT_TYPE(query));

const autoCompleteResponse = response?.data?.map((item: any) =\> {

return {

label: item?.type_name ?? \'\',

value: item?.id ?? \'\',

};

});

return autoCompleteResponse;

};

**After:**

TypeScript

export const EmploymentType = async (query: string) =\> {

const response: any = await
apiClient.get(API_ENDPOINTS.AUTOCOMPLETE.EMPLOYMENT_TYPE(query));

const autoCompleteResponse = response?.data?.map((item: any) =\> {

return {

// Prioritizes the new key, falls back to the old one

label: item?.arrangement_type ?? item?.type_name ?? \'\',

value: item?.id ?? \'\',

};

});

return autoCompleteResponse;

};

## **2. Removing the Search Input from the Dropdown**

**The Problem:**

The \"Job Type\" modal was rendering a text search bar. Since the new
endpoint only returns three static options (remote, onsite, hybrid), the
search functionality was unnecessary and cluttered the UI.

**The Solution:**

Because the AutocompleteField component was already built to handle
different display modes dynamically, we didn\'t need to rewrite any UI
rendering logic. We simply updated the configuration object passed to
the FormInput inside the specific screen, changing the searchable flag
from true to false. This automatically triggered the component\'s
built-in \"bottom-sheet\" style without affecting other dropdowns (like
\"Location\").

**File Modified:** \* src/screens/\.../CreateJob.tsx (or your specific
screen path)

## **Code Snippets: src/screens/\.../CreateJob.tsx**

**Before:**

TypeScript

\<FormInput

config={{

type: \'autocomplete\',

control,

name: \'jobType\',

// \...

searchable: true,

searchType: \'employmentType\',

}}

/\>

**After:**

TypeScript

\<FormInput

config={{

type: \'autocomplete\',

control,

name: \'jobType\',

// \...

searchable: false, // Disables search input and triggers bottom-sheet UI

searchType: \'employmentType\',

}}

/\>

## **Best Practices for Future Reference**

- **Defensive Data Mapping (Backward Compatibility):** When a backend
  API changes its response keys (e.g., type_name to arrangement_type),
  chaining nullish coalescing operators (item?.newKey ?? item?.oldKey ??
  \'fallback\') is a highly effective way to prevent the app from
  breaking. It ensures that if users have cached data or if another part
  of the app hasn\'t caught up to the API change, the UI will still
  render correctly.

- **Centralized API Definitions:** Keeping all raw URL strings in an
  endpoints.ts file means you never have to hunt through components to
  find where an API call is being made. You update the route in one
  place, and the entire app respects it.

- **Prop-Driven UI Variations:** Your AutocompleteField.tsx is an
  excellent example of a robust component. By passing a simple boolean
  (searchable: false), it handles complex conditional styling (removing
  the search bar, dimming the background, changing the modal height).
  This keeps your screen files (CreateJob.tsx) clean and declarative.

# Problem 70

Here is a quick summary of the issue and the exact code snippets you
need for your future reference.

![](data/media_dump/media/image2.png){width="2.0656955380577426in"
height="4.328125546806649in"}![](data/media_dump/media/image8.png){width="1.995916447944007in"
height="4.338542213473316in"}

## **The Issue**

You need to dynamically control the vertical spacing below a text input
field in a React Native app. Specifically, you wanted different spacing
when the user is actively typing (keyboard open) versus when the input
is idle (keyboard closed), without breaking the existing layout or
affecting other screens that use the same shared component.

## **Files Involved**

1.  **components/common/CommentInput.tsx**: The shared reusable
    component containing the actual text input.

2.  **PostDetail.tsx**: The parent screen that renders the post,
    comments, and the CommentInput component at the bottom.

## **Important Code Snippets for Future Reference**

#### **1. Making the Shared Component Safely Customizable**

**File:** components/common/CommentInput.tsx

*The Fix: Added an optional containerStyle prop to allow the parent
screen to override default padding without breaking backward
compatibility.*

TypeScript

import { View, StyleSheet, TextInput, StyleProp, ViewStyle } from
\'react-native\';

type Props = {

onSubmit: (text: string) =\> Promise\<void\> \| void;

// \... other props

containerStyle?: StyleProp\<ViewStyle\>; // \<\-- Added this

};

export default function CommentInput({ onSubmit, containerStyle,
\...rest }: Props) {

return (

// Applied the custom style to the outermost View

\<View style={\[styles.container, containerStyle\]}\>

{/\* \... existing input code \... \*/}

\</View\>

);

}

#### **2. Tracking Keyboard Visibility**

**File:** PostDetail.tsx

*The Fix: Added a state and standard React Native keyboard listeners
inside a useEffect to know exactly when the keyboard is open or closed.*

TypeScript

import { Keyboard, Platform } from \'react-native\';

// \... inside your component:

const \[isKeyboardVisible, setIsKeyboardVisible\] =
React.useState(false);

React.useEffect(() =\> {

const showSubscription = Keyboard.addListener(

Platform.OS === \'ios\' ? \'keyboardWillShow\' : \'keyboardDidShow\',

() =\> setIsKeyboardVisible(true) // Keyboard is OPEN

);

const hideSubscription = Keyboard.addListener(

Platform.OS === \'ios\' ? \'keyboardWillHide\' : \'keyboardDidHide\',

() =\> setIsKeyboardVisible(false) // Keyboard is CLOSED

);

return () =\> {

showSubscription.remove();

hideSubscription.remove();

};

}, \[\]);

#### **3. Applying Dynamic Spacing based on Keyboard State**

**File:** PostDetail.tsx

*The Fix: Removed static paddingBottom from the stylesheet and used
inline conditional logic to control both the outer and inner spacing.*

TypeScript

\<View

style={\[

styles.footerContainer,

{

// Outer spacing (Space below the whole container)

paddingBottom: isKeyboardVisible

? 0 // Value when typing

: (insets.bottom \> 0 ? insets.bottom : theme.spacing.md) // Value when
idle

}

\]}

\>

\<CommentInput

onSubmit={handleCreateComment}

// Inner spacing (Padding inside the input block itself)

containerStyle={{

paddingBottom: isKeyboardVisible

? theme.spacing.xs // Value when typing

: theme.spacing.md // Value when idle

}}

/\>

\</View\>

# Problem 71\
I\'m glad to hear that fixed it! Keeping a record of these kinds of bugs
is a great practice.

Here is a summary of the two root causes, along with the files and the
before-and-after code snippets for your future reference.

## **1. The Data Parsing Bug (Silent Failure)**

**File:** DocumentsTab.tsx (or your document list component)

**The Problem:** The frontend was expecting the uploaded document
objects (which contain the fileUrl and fileName) to be under the
otherUrl key. However, the backend returned an array of integer IDs for
otherUrl and put the actual file objects under a new key called
otherDocs. Because integers don\'t have a .fileUrl property, the
frontend silently filtered them out and showed an empty list.

**Before:**

TypeScript

const otherDocs = rawData.otherDocuments \|\| rawData.otherUrl \|\|
rawData.others \|\| \[\];

**After:**

TypeScript

// Added rawData.otherDocs to capture the correct array of objects

const otherDocs = rawData.otherDocs \|\| rawData.otherDocuments \|\|
rawData.otherUrl \|\| rawData.others \|\| \[\];

## **2. The React Query Cache Bug (Stale UI)**

**File:** AddDocumentModal.tsx (or your upload component)

**The Problem:**

After a successful upload, the modal tried to tell React Query to
refetch the document list. However, it used the query key
\[queryKeys.company.getCompanyDocuments\]. Because the original hook
(useGetCompanyDocuments) fetched data using an array that included the
specific ID (\[queryKeys.company.getCompanyDocuments, companyId\]), the
keys didn\'t match perfectly. React Query ignored the invalidation,
leaving the UI showing the old, cached empty list until the app was
manually refreshed.

**Before:**

TypeScript

queryClient.invalidateQueries({ queryKey:
\[queryKeys.company.getCompanyDocuments\] });

**After:**

TypeScript

// Appended companyId to match the hook\'s exact queryKey array

queryClient.invalidateQueries({ queryKey:
\[queryKeys.company.getCompanyDocuments, companyId\] });

# Problem 72

That was a solid debugging session! You methodically tracked down a
missing API call, wired up the UI, and then correctly diagnosed and
fixed a tricky data-mapping issue causing a server crash.

Here is a complete summary of the problem, the code changes, and best
practices so you have a clean reference for the future.

## **The Problem Summary**

This bug happened in two phases:

1.  **The \"Silent\" Delete:** Initially, tapping the delete button did
    nothing. The confirmation alert popped up, but the onPress action
    was just an empty function () =\> {}. There was no API hook wired up
    to tell the backend to actually delete the file.

2.  **The 500 Internal Server Error:** After wiring up the correct
    useDeleteDocument hook, the backend crashed with a Status 500
    (invalid input syntax for type integer). This happened because the
    backend wasn\'t putting the database id inside the document objects
    (otherDocs). Because the frontend couldn\'t find an ID, it generated
    a fallback string (e.g., \"other-0\"). The backend expected a real
    integer ID (like 999), so it panicked when it received the string.

**The Fix:** We had to extract the real integer IDs, which the backend
was sending in a parallel array called otherUrl, and map them to the
documents using their index.

## **Files Modified**

- src/api/services/upload.service.ts (Added the API call)

- src/api/hooks/useUpload.ts (Created the React Query hook)

- DocumentsTab.tsx (Wired the hook to the UI, updated the cache, and
  fixed the data mapping)

## **Code Snippets: Before & After**

#### **1. The API Setup (New Additions)**

Before, the app had no way to delete documents. We added the service and
the hook.

**After:**

TypeScript

// src/api/services/upload.service.ts

export const deleteDocument = async (id: string \| number) =\> {

return await apiClient.delete(API_ENDPOINTS.UPLOAD.DELETEDOCUMENT(id));

};

// src/api/hooks/useUpload.ts

import { deleteDocument } from \'../services/upload.service\';

export const useDeleteDocument = () =\> {

return useMutation({

mutationFn: (id: string \| number) =\> deleteDocument(id),

});

};

#### **2. The UI Wiring (DocumentsTab.tsx)**

Before, the handleDelete function triggered an empty onPress.

**❌ Before:**

TypeScript

{

text: \'Delete\',

style: \'destructive\',

onPress: () =\> { } // Did nothing

}

**✅ After:**

We passed down an executeDelete function that calls the mutation and
refreshes the document list (queryClient.invalidateQueries) upon
success.

TypeScript

{

text: \'Delete\',

style: \'destructive\',

onPress: () =\> onDelete(document.id) // Triggers the backend call

}

#### **3. The 500 Error Fix (Data Mapping)**

Before, the frontend mapped the documents but generated fake string IDs
because it didn\'t look at the otherUrl array.

**❌ Before:**

TypeScript

const otherDocs = rawData.otherDocs \|\| rawData.otherDocuments \|\|
rawData.otherUrl \|\| rawData.others \|\| \[\];

if (Array.isArray(otherDocs)) {

otherDocs.forEach((doc: any, index: number) =\> {

if (doc.fileUrl \|\| doc.url) {

result.push({

// BUG: doc.id is undefined, so it sends \"other-0\" to the backend

id: doc.id \|\| \`other-\${index}\`,

documentName: doc.originalName \|\| doc.fileName \|\| doc.name \|\|
\`Other Document \${index + 1}.pdf\`,

size: doc.size \|\| 0,

fileUrl: doc.fileUrl \|\| doc.url,

});

}

});

}

**✅ After:**

We separated the document array from the ID array and used the loop\'s
index to marry them together.

TypeScript

// Separate the actual documents array from the IDs array

const otherDocs = rawData.otherDocs \|\| rawData.otherDocuments \|\|
rawData.others \|\| \[\];

const otherUrlIds = Array.isArray(rawData.otherUrl) ? rawData.otherUrl :
\[\];

if (Array.isArray(otherDocs)) {

otherDocs.forEach((doc: any, index: number) =\> {

if (doc.fileUrl \|\| doc.url) {

// SOLUTION: Grab the real ID from the parallel array using the index

const realUploadId = otherUrlIds\[index\];

result.push({

// Sends the real ID (e.g., 999) safely to the backend

id: realUploadId \|\| doc.id \|\| \`other-\${index}\`,

documentName: doc.originalName \|\| doc.fileName \|\| doc.name \|\|
\`Other Document \${index + 1}.pdf\`,

size: doc.size \|\| 0,

fileUrl: doc.fileUrl \|\| doc.url,

});

}

});

}

## **Best Practices for Future Reference**

- **Never trust frontend-generated IDs for backend mutations:** It is
  totally fine to use generated strings (like \"other-0\") as key props
  for React lists. However, when performing a DELETE, PUT, or POST, you
  must ensure you are sending the exact database identifier the backend
  expects.

- **Investigate 500 Errors at the Payload Level:** A Status 500 often
  means the backend choked on the format of the data you sent. If you
  hit a 500 error, immediately check the network request payload (URL
  params or body) to ensure data types (string vs. integer) match the
  backend\'s expectations.

- **Beware of Parallel Arrays:** While you have to work with the API you
  are given, sending data across parallel arrays (e.g., otherUrl for IDs
  and otherDocs for file info) is risky. If the arrays ever get out of
  sync, you could delete the wrong file. Keep an eye on this if your
  backend team ever updates that endpoint!

# Problem 73

Here is a summary of the issue and the solution for your future
reference:

## **Problem Summary**

1.  **Raw Backend Errors Exposed:** The application was directly
    displaying the raw backend API error message (\"Text contains
    disallowed language (\\\"\[word\]\\\").\") to the user via a toast
    whenever profanity was detected.

2.  **Text Truncation:** When the message was updated to a more
    professional, longer string (\"Your text may contain language that
    violates our community guidelines.\"), the text got cut off at the
    end because the global toast UI component had a hard limit on the
    number of lines it could display.

## **The Solution & Important Files**

#### **1. Intercepting the Error Message**

**File:** src/api/config.ts (or your Axios/API configuration file)

**What we did:** We modified the global response interceptor
(apiClient.interceptors.response.use) to catch the specific backend
error string *before* it gets passed to the toast function.

**Important Code Snippet:**

TypeScript

// Inside apiClient.interceptors.response.use (error block):

let errorMessage = error.response?.data?.message \|\| error.message \|\|
\'Something went wrong\';

// Intercept the specific profanity error from the backend

if (typeof errorMessage === \'string\' &&
errorMessage.includes(\'disallowed language\')) {

errorMessage = \'Your text may contain language that violates our
community guidelines.\';

}

if (errorMessage !== \'Access token required\') {

toast.error(errorMessage);

}

#### **2. Fixing the Truncated UI**

**File:** src/components/toast/SnackbarProvider.tsx

**What we did:** We increased the numberOfLines prop on the React Native
\<Text\> component inside the Snackbar from 2 to 3 to allow longer
messages to wrap properly.

**Important Code Snippet:**

TypeScript

{/\* Increased numberOfLines to prevent text cutoff \*/}

\<Text style={styles.message} numberOfLines={3} ellipsizeMode=\"tail\"\>

{message}

\</Text\>

## **Why this implementation works well:**

- **Global Coverage:** Because the text replacement happens in the Axios
  interceptor, this custom profanity warning will automatically apply to
  *any* API call in the app (creating a post, leaving a comment, editing
  a profile, etc.) that triggers that specific backend error.

- **Backward Compatible:** It safely checks for a specific string
  (\"disallowed language\"). All other API errors (like 500s or 404s)
  bypass this override and display normally.

# Problem 74

**The Problem Summary**

1.  **The node_modules Trap:** You are currently editing the internal
    source code of a third-party library. If you run npm install
    tomorrow, all your layout fixes will be instantly deleted.

2.  **The Layout Quirks:** \* *Horizontal:* React Native is letting the
    physical width of the word \"Community\" stretch its column, pushing
    the other icons off-center.

    - *Vertical:* The icons are centering themselves based on their
      unique shapes rather than hanging perfectly straight from the top
      edge.

    - *Padding:* The IconButton from React Native Paper is adding
      invisible margins that fight against your flex grid.

**My Recommendation: What to do first**

**Absolutely move to your src/ folder first.** Stop fighting the
library\'s complex internal files.

If you try to fix the layout inside node_modules first, you are dealing
with thousands of lines of advanced library code that you didn\'t write,
just to tweak a few flexbox rules.

Here is the best path forward:

1.  **Hit the Reset Button:** Run that git restore command to wipe out
    the changes in node_modules. Let React Navigation go back to its
    default state.

2.  **Make a Fresh Component:** Create a brand new file like
    src/components/CustomTabBar.tsx.

3.  **Build It Clean:** React Navigation gives you the state and
    descriptors props to build your own bar. We will build a simple,
    clean row of buttons applying the exact flexbox rules we just talked
    about (flexBasis: 0, justifyContent: \'flex-start\', etc.).

4.  **Plug It In:** Tell your MainNavigator.tsx to use your new custom
    bar instead of the default one.

By doing it this way, you take complete control of the layout, your code
is 10x easier to read, and your fixes are permanent.

Would you like me to write the code for a clean, fully aligned
CustomTabBar.tsx that you can just copy, paste, and plug right into your
navigator?

Here is the complete list of files and their exact locations that we
have discussed during this troubleshooting process, categorized for easy
reference:

**The Library Files (Inside node_modules)**

*These are the files you temporarily modified to test the flexbox
layout, which should be reverted using npm install or yarn install.*

- node_modules/@react-navigation/bottom-tabs/src/views/BottomTabBar.tsx

- node_modules/@react-navigation/bottom-tabs/src/views/BottomTabItem.tsx

**Your Existing Project Files (Inside src)**

*These are the files that belong to your app and are safe to modify and
commit.*

- src/utils/Icons.tsx (Where your IconButton components are defined and
  where we removed the default margins)

- src/navigation/MainNavigator.tsx (Where your Tab.Navigator is
  initialized)

**The Recommended Future File**

*This is the file you should create to implement your layout fixes
permanently and safely.*

- src/components/CustomTabBar.tsx (The ideal location to build your
  custom tab bar component)

Here is a complete summary of exactly how you permanently solved the
layout bug, including the files you created, the files you modified, and
the key code snippets.

**#SOLUTION:**

## **The Core Problem You Solved**

Your tab bar was suffering from two competing layout issues:

1.  **Horizontal Stretching:** React Native\'s flexbox allowed wide text
    labels (like \"Community\") to stretch their columns, pushing other
    icons off-center.

2.  **Vertical Misalignment:** React Native Paper's \<IconButton\> has
    an invisible 48x48 pixel touch target. This hidden padding was
    fighting your layout, causing icons and text to misalign.

Instead of fighting the node_modules code, you built a pristine,
custom-controlled layout.

## **Step 1: You Built a Custom Tab Bar**

**File Created:** src/components/common/CustomBottomTabBar.tsx

You created a fully custom component to take total control over the
flexbox grid.

- You used flexBasis: 0 to force every single column to be
  mathematically identical in width, regardless of how long the text
  label was.

- You implemented your dynamic active/inactive color scheme (#FA6400 for
  active, #9CABBA for inactive).

**Key Snippet:**

TypeScript

// Inside CustomBottomTabBar.tsx

// 1. The custom color logic for icons and text:

const color = isFocused ? \'#FA6400\' : \'#9CABBA\';

// 2. The critical flexbox styles:

const styles = StyleSheet.create({

container: {

flexDirection: \'row\',

borderTopWidth: StyleSheet.hairlineWidth,

borderTopColor: \'rgba(0, 0, 0, 0.1)\',

paddingTop: 8,

},

tabItem: {

flex: 1,

flexBasis: 0, // CRITICAL: Forces strictly equal column widths

alignItems: \'center\',

justifyContent: \'flex-start\', // Anchors everything from the top down
evenly

},

iconWrapper: {

position: \'relative\',

alignItems: \'center\',

justifyContent: \'center\',

height: 32, // Gives the icons a consistent bounding box

},

// \... badge and label styles

});

## **Step 2: You Stripped the Hidden Icon Margins**

**File Modified:** src/utils/Icons.tsx

To prevent existing parts of your app from breaking (The Golden Rule of
Backward Compatibility), you left your old \<IconButton\> methods alone.
Instead, you imported the raw, padding-free \<Icon\> component from
react-native-paper and created specific Tab Bar functions.

**Key Snippet:**

TypeScript

import { IconButton, Icon } from \'react-native-paper\';

class Icons {

// \-\-- NEW TAB BAR ICONS (NO PADDING) \-\--

static renderTabBarHomeIcon(color: string): JSX.Element {

return \<Icon source=\"home-outline\" color={color} size={24} /\>;

}

static renderTabBarSearchIcon(color: string): JSX.Element {

return \<Icon source=\"magnify\" color={color} size={24} /\>;

}

static renderTabBarCommunityIcon(color: string): JSX.Element {

return \<Icon source=\"account-supervisor-outline\" color={color}
size={24} /\>;

}

static renderTabBarInactiveChatIcon(color: string): JSX.Element {

return \<Icon source=\"chat-outline\" color={color} size={24} /\>;

}

static renderTabBarCalendarIcon(color: string): JSX.Element {

return \<Icon source=\"calendar-month-outline\" color={color} size={24}
/\>;

}

// \... old IconButton methods remained untouched below

}

## **Step 3: You Wired It All Together**

**File Modified:** src/navigation/MainNavigator.tsx

Finally, you told React Navigation to stop using its default layout and
default icons, and to use your new custom code instead. You did this for
both \<Tab.Navigator\> instances (MainNavigator and
MainInvestorNavigator).

**Key Snippet:**

TypeScript

import { CustomBottomTabBar } from
\'@/components/common/CustomBottomTabBar\';

// 1. Injected the custom tab bar UI:

\<Tab.Navigator

tabBar={props =\> \<CustomBottomTabBar {\...props} /\>}

screenOptions={{ \... }}

\>

\<Tab.Screen

name={SCREEN_NAMES.HOME}

component={HomeScreenPage}

options={{

title: t(TAB_KEYS.HOME),

// 2. Swapped to the new, padding-free icons:

tabBarIcon: props =\> Icons.renderTabBarHomeIcon(props.color),

tabBarLabel: t(TAB_KEYS.HOME),

}}

/\>

// \... applied to all other screens

\</Tab.Navigator\>

## **Final Step (Cleanup)**

Because you moved all this logic safely into your src/ folder, your
final step is to simply run npm install (or yarn install \--force) to
wipe out any temporary experiments you made inside the node_modules
folder, ensuring your project is totally clean.

# Problem 75\
Here is a complete summary of the problems we tackled, the files
involved, and the solutions we implemented for your future reference.

### **Target File**

- **Main File Modified:**
  src/screens/community/components/community-dashboard/TabScreen/QuestionU.tsx

### **Issue 1: Swapping Username and Community Name UI**

- **Problem:** The UI displayed the community prefix (e.g., c/Mikasa)
  small and on top, and the user\'s name (e.g., Mikasa Ackerman) large
  and bold on the bottom. You wanted to reverse their positions and
  sizes.

- **Solution:** We swapped the order of the \<Text\> components inside
  the userInfoContainer and swapped the styles applied to them.

- TypeScript

// The prefix now uses the larger, bold style (userName)

\<Text style={styles.userName}\>{question.author.prefix}\</Text\>

// The user\'s name now uses the smaller style (userPrefix)

\<Text style={styles.userPrefix}\>{question.author.name}\</Text\>

- 
- 

### **Issue 2: Displaying Community Icon instead of User Avatar**

- **Problem:** You wanted to replace the user\'s profile picture with
  the community\'s icon if the endpoint provided it.

- **Investigation:** By logging the API response, we discovered the
  backend is currently *not* sending a community icon field for
  questions (it only sends the user\'s avatar_url).

- **Solution:** We set up the frontend to be ready for the data once the
  backend adds it (Backward Compatibility).

  - Added an optional community_icon_url?: string; to the
    Question\[\'author\'\] TypeScript interface.

  - Updated getAvatarSource to prioritize the community icon, falling
    back to the user avatar if it\'s missing:

- TypeScript

const getAvatarSource = () =\> {

const iconUrl = question.author.community_icon_url \|\|
question.author.avatar_url;

if (avatarError \|\| !iconUrl) return Images.avatarDefault as any;

return { uri: iconUrl };

};

- - *Action Item pending:* The backend team needs to add
    community_icon_url to the questions API response.

### **Issue 3: Independent Navigation to User Profile**

- **Problem:** Clicking anywhere on the card navigated to the
  CommunityQuestionDetail screen. You wanted clicking specifically on
  the user\'s name to navigate to their profile (UserProfile).

- **Solution:** 1. Imported TouchableOpacity.\
  2. Wrapped the \<Text\> component for the user\'s name in a
  \<TouchableOpacity\> with a new onUserPress trigger.\
  3. Created a handleUserPress function in the main QuestionU component
  using React Navigation.

### **Issue 4: API Error (400 Invalid Profile ID) on Navigation**

- **Problem:** Clicking the user\'s name triggered a red error screen
  saying \"Invalid profile id provided\".

- **Investigation:** We realized the API response contained two IDs for
  the author: a numeric id (e.g., 111) and a UUID userId (e.g.,
  \"d0c\...ca78\"). We were passing the UUID, but the backend\'s profile
  endpoint expected the numeric id.

- **Solution:** Changed the ID passed into the onUserPress handler from
  userId to id.toString().

- TypeScript

// Changed from question.author.userId to question.author.id.toString()

\<TouchableOpacity onPress={() =\>
onUserPress(question.author.id.toString())}\>

\<Text style={styles.userPrefix}\>{question.author.name}\</Text\>

\</TouchableOpacity\>

- 
- 

### **Final Architecture Notes**

Your QuestionCard component now takes onUserPress as a prop alongside
onPress. This safely separates the \"Card Click\" (goes to Question
Details) from the \"Author Click\" (goes to User Profile) without
breaking existing layout styles.

# Problem 76

Here is a complete summary of the issue, the solution, and the best
practices we followed. You can use this as documentation or a commit
message reference for your team.

### **📌 Problem Summary**

We needed to replace a custom-built, horizontally scrolling tab bar in
the Community Detail screen with the standard
\@react-navigation/material-top-tabs to match the exact behavior and
shifting animation used on the Profile screen.

However, upon implementation, the new tabs completely disappeared from
the screen. This happened because the parent container
(styles.detailContainer) had alignItems: \'center\' applied to it. In
React Native\'s flexbox engine, this forces child components to shrink
to their minimum required width. Since the Material Top Tab navigator is
designed to dynamically fill available space, the parent container
forced it to collapse to a width of 0.

### **📁 Files Involved**

- **src/screens/community/CommunityDetail.tsx**: The primary file where
  the Tab Navigator was implemented and fixed.

- **src/screens/profile/Profile.tsx**: Used as the reference
  architecture for how tabs should behave.

- **src/screens/community/communityStyles.ts**: (Untouched) Contained
  the alignItems: \'center\' rule that caused the flexbox conflict.

### **💻 Important Code Snippets**

**The Issue (Invisible Tabs):**

TypeScript

In: src/screens/community/CommunityDetail.tsx

{/\* Inherits alignItems: \'center\' from the parent, causing width to
collapse to 0 \*/}

\<View style={{ minHeight: Dimensions.get(\'window\').height }}\>

\<Tab.Navigator

screenOptions={{

tabBarStyle: {

// \... other styles

}

}}

\>

**The Fix (Overriding the constraint):**

TypeScript

{/\* Added width: \'100%\' and flex: 1 to force the wrapper to stretch
\*/}

\<View style={{ minHeight: Dimensions.get(\'window\').height, width:
\'100%\', flex: 1 }}\>

\<Tab.Navigator

screenOptions={{

tabBarStyle: {

width: \'100%\', // \<\-- Ensures the tab bar itself stretches
edge-to-edge

// \... other styles

}

}}

\>

### **🧠 Why We Chose This Approach**

1.  **Standardization:** We are already using
    \@react-navigation/material-top-tabs in Profile.tsx. Standardizing
    on one library across the app reduces bundle size, makes maintenance
    easier, and ensures a consistent user experience (UX) with the
    auto-shifting animation.

2.  **Zero-Impact Refactoring (Golden Rule):** Instead of rewriting
    communityStyles.ts and removing alignItems: \'center\' from
    detailContainer (which could have unpredictably broken the layout of
    the community image, title, and buttons above the tabs), we applied
    an inline override width: \'100%\' strictly to the tab wrapper. This
    ensured **100% backward compatibility** with the rest of the
    screen\'s UI.

3.  **Nested Scroll Architecture:** By wrapping the Tab Navigator in a
    View with a minHeight equal to the device window\'s height, we
    successfully nested a tabbed navigator inside a parent ScrollView
    without causing scrolling conflicts.

### **🚀 Best Practices for Future Reference**

- **Beware of alignItems: \'center\' on Wrappers:** When building
  screens, avoid putting alignItems: \'center\' on the outermost
  container if that container holds full-width fluid components (like
  lists, navigators, or maps). It is usually safer to let the parent
  stretch (alignItems: \'stretch\', which is the default) and center
  individual child elements as needed.

- **Inline Overrides for Safe Hotfixes:** When migrating isolated
  components inside legacy screens, use inline style overrides (like
  width: \'100%\') to fix flexbox issues rather than refactoring shared
  stylesheet objects. This prevents cascading UI bugs across other
  components that share that style.

- **Use Functional Wrappers for Route Params:** Just like in
  ProfileTopTabs.tsx, if you need to pass parent state or route
  parameters down to screens inside a Tab.Navigator, passing an inline
  arrow function to the children prop (e.g., \<Tab.Screen\>{() =\>
  \<MyComponent /\>}\</Tab.Screen\>) is a clean and effective pattern.

# Problem 77

Here is a summary of the problem, the investigation process, and the
final solution for your future reference.

### **The Problem**

You needed to add an **\"(Edited)\" indicator** and a **formatted
timestamp** to an AnswerCard component in a React Native app. The goal
was to show when a post was originally created and indicate if it had
been modified, without breaking any existing UI styles or causing
crashes if the data was missing.

### **The Investigation**

Before writing any UI code, we had to verify if this was a frontend or
backend task.

1.  **Frontend vs. Backend:** It requires both. The backend must track
    the dates, and the frontend must compare them.

2.  **Data Verification:** We temporarily added console.log(\'DEBUG
    ANSWER DATA:\', answer); to AnswerCard.tsx to inspect the API
    payload.

3.  **The Discovery:** The logs confirmed the backend was already
    sending both createdAt and updatedAt in ISO 8601 format (e.g.,
    \'2026-03-27T14:41:43.537Z\').

### **The Solution**

We implemented the logic entirely on the frontend by comparing the
createdAt and updatedAt timestamps. If updatedAt is greater than
createdAt, the post is marked as edited. We appended the text \" •
Edited\" directly inside the existing date \<Text\> component to inherit
all current styles seamlessly.

#### **Important Code Snippets**

**1. The Comparison Logic (Added inside the component before the return
statement):**

We used React.useMemo to ensure the calculation only runs when the
timestamps change, optimizing performance. We also added fallback checks
(if (!createdAt \|\| !updatedAt)) to ensure backward compatibility in
case the API ever fails to send these fields.

TypeScript

// 1. EXTRACT TIMESTAMPS

const createdAt = answer.createdAt;

const updatedAt = answer.updatedAt;

// 2. DETERMINE IF EDITED

// Compare the two timestamps. If updatedAt is later than createdAt,
it\'s edited.

const isEdited = React.useMemo(() =\> {

if (!createdAt \|\| !updatedAt) return false;

return new Date(updatedAt).getTime() \> new Date(createdAt).getTime();

}, \[createdAt, updatedAt\]);

**2. The UI Implementation (Inside the JSX return):**

We placed the formatted date and the conditional \"Edited\" string
inside the same \<Text\> wrapper. This prevented the need to write new
CSS or alter the existing AnswerCardStyles.

TypeScript

{/\* 3. UPDATED JSX TO SHOW DATE AND EDITED INDICATOR \*/}

\<Text style={styles.dateText}\>

{formatDate(createdAt)}

{isEdited && \' • Edited\'}

\</Text\>

### **Key Takeaways for Future Features**

- **Always verify the data first:** Logging the API response saved us
  from building UI for data that might not have existed.

- **Preserve styles by grouping text:** Appending strings inside a
  single \<Text\> node in React Native is the safest way to maintain
  font families, colors, and line heights without writing new stylesheet
  rules.

- **Fail gracefully:** The if (!createdAt \|\| !updatedAt) return false;
  line is the \"Golden Rule\" in action---if the data is missing, the
  app just assumes the post isn\'t edited, rather than crashing with a
  null reference error.

# Problem 78\
Here is a complete summary of the feature implementation for your future
reference.

# **Feature Summary: \"Follow Question\" Toggle**

## **1. The Problem**

You needed to transition a static \"Follow this Question\" menu option
in a React Native application into a fully functional feature. The app
uses a custom apiClient and \@tanstack/react-query for state management.

The goal was to:

1.  Hit a backend API to toggle the follow state.

2.  Update the UI text dynamically (\"Follow\" vs \"Unfollow\").

3.  Refresh the UI automatically without requiring a full page reload or
    interrupting the user experience.

## **2. The Missing Piece**

Before writing the code, we identified the exact backend API contract
required to perform the action:

- **Endpoint:** /api/v1/qa/questions/:id/follow

- **Method:** POST

- **Payload:** None (Toggles state based on the URL ID).

## **3. The Architecture (Files Modified)**

We implemented a complete \"Mutation Flow\" across 5 layers of your
frontend architecture:

### **Step 1: Define the Endpoint**

**File:** src/api/endpoints.ts

Added the URL path to centralized endpoint configurations.

TypeScript

QUESTION_ANSWER: {

// \... existing endpoints

FOLLOW_QUESTION: (questionId: string \| number) =\>
\`/qa/questions/\${questionId}/follow\`,

},

### **Step 2: Register the Query Key**

**File:** src/api/queryKeys.ts

Added a unique key for caching and invalidation purposes.

TypeScript

questionAnswer: {

// \... existing keys

followQuestion: \[\'apps\', \'questionAnswer\', \'followQuestion\'\],

},

### **Step 3: Create the API Service**

**File:** src/api/services/question.answer.service.ts

Created the function that actually communicates with the backend using
your custom client.

TypeScript

export const FollowQuestion = async (questionId: string \| number) =\> {

return await
apiClient.post(API_ENDPOINTS.QUESTION_ANSWER.FOLLOW_QUESTION(questionId));

};

### **Step 4: Create the React Query Hook (The \"Magic\")**

**File:** src/api/hooks/useQuestionAnswer.ts

Wrapped the service in a useMutation hook. The onSuccess block is
crucial here: it tells React Query to immediately re-fetch the specific
question\'s data in the background, which updates the UI state
automatically.

TypeScript

export const useFollowQuestion = () =\>

useMutation({

mutationKey: \[queryKeys.questionAnswer.followQuestion\],

mutationFn: (questionId: string \| number) =\>
FollowQuestion(questionId),

onSuccess: async (\_data, questionId) =\> {

// Automatically refresh the question details

queryClient.invalidateQueries({

queryKey: \[queryKeys.questionAnswer.getQuestionDetail, questionId\],

exact: true,

});

},

});

### **Step 5: Wire up the UI**

**File:** src/screens/community/QuestionDetail.tsx

Connected the hook to the UI component. We used optional props
(isQuestionFollowed and onFollowQuestionToggle) to ensure backward
compatibility for shared header components.

TypeScript

// Inside QuestionDetail component:

const { mutate: toggleFollowQuestion } = useFollowQuestion();

const isQuestionFollowed = pathOr(false, \[\'data\', \'is_followed\'\],
questionDetailData);

const handleFollowQuestionToggle = () =\> {

if (questionId) toggleFollowQuestion(questionId);

};

// Passed to the header:

\<QuestionTopHeader

navigation={navigation}

isQuestionFollowed={isQuestionFollowed}

onFollowQuestionToggle={handleFollowQuestionToggle}

/\>

## **4. The Final Polish (Fixing the Spinner)**

Because queryClient.invalidateQueries triggers a background fetch,
isQuestionDetailFetching temporarily becomes true. Initially, this was
tied directly to the \<RefreshControl\>, causing a pull-to-refresh
spinner to flash every time the user followed a question.

**The Solution:** We decoupled background fetching from manual
refreshing by creating a dedicated isManualRefresh state for the
\<RefreshControl\>.

TypeScript

// Created isolated state for manual user pull-to-refresh

const \[isManualRefresh, setIsManualRefresh\] = useState(false);

const handlePullToRefresh = async () =\> {

setIsManualRefresh(true);

await refetchQuestionDetail();

setIsManualRefresh(false);

};

// Applied to ScrollView

\<ScrollView

refreshControl={

\<RefreshControl refreshing={isManualRefresh}
onRefresh={handlePullToRefresh} /\>

}

\>

**Outcome:** The user can now follow/unfollow a question seamlessly. The
request hits the backend, the data updates silently in the background,
and the menu text changes instantly---all with no visual interruption.

# Problem 79

Here is a summary of exactly what we did, the key code changes, and the
best practices you can take away from this implementation for the
future.

### **1. Files Modified & Key Code Changes**

**File:
src/screens/community/components/community-dashboard/TabScreen/MyCommunities.tsx**

- **Added Filter UI:** We introduced a new pageHeaderContainer and a
  Modal to handle the dropdown UI without affecting the layout below it.

- **Dynamic Data Passing:** We updated the FlatList\'s renderItem to
  safely extract the user\'s role and pass it as a specific label.

- TypeScript

// Inside renderItem

const role = pathOr(\'member\', \[\'membership\', \'role\'\],
item).toLowerCase();

const tagLabel = (role === \'owner\' \|\| role === \'admin\') ?
\'Admin\' : \'Member\';

\<CommunityCard roleTag={tagLabel} /\> // Passing the new prop

- 

- 

- **Fixed the Cutoff Issue (Flexbox):** We removed the hardcoded width:
  \'75%\' on the name text and replaced it with flex: 1. This allowed
  the title to shrink dynamically and let the tags breathe on the right
  side.

- **Fixed the Stacking Issue (Style Collision):** We renamed
  headerContainer to pageHeaderContainer for the top filter bar. Because
  CommunityCard also used the name headerContainer, the parent style was
  accidentally overriding the child style and forcing the text onto the
  same row.

**File: src/components/common/CommunityCard.tsx**

- **Backward Compatibility:** We added roleTag?: string; as an
  *optional* prop. This ensured the card didn\'t break on other screens
  where the tag wasn\'t needed.

- **Localized Tag Styling:** We created a getRoleTagStyles(role)
  function inside the component to handle the specific orange (Admin)
  and grey (Member) background colors dynamically.

- **Layout Wrapper:** We wrapped the Community Name and the Tag in a
  standard flex row:

- TypeScript

\<View style={{ flexDirection: \'row\', justifyContent:
\'space-between\', alignItems: \'center\' }}\>

\<Text style={\[styles.name, roleTag && { width: \'auto\', flex: 1,
paddingRight: 8 }\]} numberOfLines={1}\>

{community.name}

\</Text\>

{roleTag && (

\<View style={getRoleTagStyles(roleTag).container}\>

\<Text style={getRoleTagStyles(roleTag).text}\>{roleTag}\</Text\>

\</View\>

)}

\</View\>

- 
- 

### **2. The Core Solutions (Why it broke and how we fixed it)**

- **The Right-Side Cutoff:** Fixed widths like width: \'75%\' are rigid.
  If the remaining 25% isn\'t enough for the new tags, the UI breaks.
  Replacing it with flex: 1 tells React Native: *\"Let the tags take
  exactly as much space as they need, and give all the remaining
  leftover space to the title.\"*

- **The Line-Break Failure:** React Native passes down styles. If a
  parent container has a style named styles.headerContainer with
  flexDirection: \'row\', and a child component uses that exact same
  class name expecting it to be a column, it causes a collision.
  Renaming the parent style isolated the layouts perfectly.

### **3. Best Practices for the Future**

1.  **The \"Golden Rule\" of Shared Components:** Whenever you modify a
    shared component like CommunityCard.tsx or a custom Button, **always
    use optional props (propName?: type)**. This guarantees you won\'t
    crash 5 other screens that don\'t know about the new feature.

2.  **Avoid Generic Style Names in Parent Files:** When building wrapper
    screens, avoid generic style names like container, header, or
    wrapper if you are passing the styles object down as a prop to
    children. Use specific names like pageHeaderContainer or
    filterWrapper to prevent accidental CSS collisions.

3.  **Flexbox \> Hardcoded Percentages:** For horizontal rows (like an
    Avatar, a Title, and an Action Button), almost always use flex: 1 on
    the middle text element instead of percentages. It makes your app
    perfectly responsive across small iPhones and large Android devices
    without calculating exact widths.

//useful command for seeing project folder structure: (tree commands)

tree -L 4 -I \"node_modules\|.git\|dist\"

tree -L 2 -I \"node_modules\"

tree src -L 4

tree -L 4 -I
\"node_modules\|.git\|dist\|android\|ios\|\_\_tests\_\_\|.expo\"

# Problem 80

Here is a detailed summary report of the issue, root cause, and solution
for your records.

### **Bug Report: Profile Action Icons Missing on Self-Navigation**

#### **1. The Problem**

When a user navigated to their own profile from the QuestionDetail
screen (by clicking either their own avatar or name on a Question or an
Answer), the top header action icons (Edit, Settings, Company) were
missing. The screen rendered as if the user was viewing a stranger\'s
profile (\"Visitor Mode\"), even though it was their own.

#### **2. Files Involved**

- **The Originating Screens:**

  - src/screens/community/QuestionDetail.tsx (Navigation trigger for the
    question author)

  - src/screens/community/components/common/AnswerCard.tsx (Navigation
    trigger for answer authors)

- **The Affected Screen (Where the fix was applied):**

  - src/screens/profile/Profile.tsx

#### **3. The Root Cause**

The Profile screen was using a flawed logic check to determine
ownership. It relied on the **presence of a navigation parameter**
rather than the **actual data returned by the API**.

Specifically, the TopHeader component used the condition
showEditButton={!userId}.

- When navigating from the bottom tab, no userId is passed, so !userId
  is true and the icons appear.

- However, when clicking a name on the Question/Answer page, the app
  explicitly passes the userId in the navigation route. Because the
  route now contained an ID, !userId became false, instantly hiding the
  edit buttons regardless of whose ID it was.

#### **4. The Solution**

The API data already contained the source of truth via the
isProfileOwner flag. The fix required updating the TopHeader logic in
Profile.tsx to stop looking at the URL parameters (!userId) and instead
use the backend-validated isOwner variable.

### **5. Key Code Snippets**

**A. How Navigation was Triggered (Context from QuestionDetail.tsx /
AnswerCard.tsx):**

TypeScript

// Explicitly passing userId caused the issue on the receiving end

navigation.navigate(\'UserProfile\', { userId: user?.id })

**B. The Flawed Logic (Before in Profile.tsx):**

TypeScript

const { userId } = useRoute\<any\>()?.params \|\| {};

// \...

const isOwner = pathOr(false, \[\'isProfileOwner\'\], UserProfileData);
// API truth (Ignored)

return (

\<TopHeader

rightComponent={

\<RightTopComponent

theme={theme}

styles={styles}

navgiation={navigation}

onEditPress={handleEditProfile}

showEditButton={!userId} // BUG: Assumes any passed ID means \"not me\"

/\>

}

/\>

// \...

)

**C. The Corrected Logic (After in Profile.tsx):**

TypeScript

const { userId } = useRoute\<any\>()?.params \|\| {};

// \...

// We extract the true ownership status from the fetched user profile
data

const isOwner = pathOr(false, \[\'isProfileOwner\'\], UserProfileData);

return (

\<TopHeader

rightComponent={

\<RightTopComponent

theme={theme}

styles={styles}

navgiation={navigation}

onEditPress={handleEditProfile}

showEditButton={isOwner} // FIX: Now relies on the API\'s validation

/\>

}

/\>

// \...

)

**Summary of Impact:** By switching to isOwner, the screen respects the
API\'s validation. If the user clicks their own post, the API recognizes
the ID belongs to the logged-in user, sets isProfileOwner to true, and
the RightTopComponent successfully renders the Edit, Settings, and
Company icons.

# Problem 81

This report details the investigation and resolution of a data mapping
discrepancy within the search functionality of the **CHIIRO Community
Mobile App**.

## **📋 Bug Report: Search Result Mapping Error**

### **1. Problem Summary**

When a user performed a search for a specific job (e.g., searching for
**\"Think\"**), the search results page displayed the **Company Name**
(\"Doggo Life\") as the primary title and a hardcoded string
(**\"Fintech\"**) as the subtitle. This made it appear as though the
search was failing to find the correct job, even though the backend was
returning the correct data.

- **Expected Behavior:** The list item should show the **Job Title**
  (\"Think\") as the main heading and the **Company Name** as the
  sub-heading.

- **Actual Behavior:** The list item showed the **Company Name** as the
  main heading and a static \"Fintech\" label.

### **2. Root Cause Analysis**

The issue was identified as a **Frontend Rendering Error** located in
the JobsSection sub-component within the Search screen.

The investigation of src/screens/search/Search.tsx revealed that the UI
was explicitly instructed to ignore the item.title field from the API
response and instead render the company name in the title slot.
Furthermore, the subtitle was hardcoded to a static string rather than
using dynamic data from the object.

#### **The \"Smoking Gun\" (Debug Logs):**

The logs confirmed that the backend was sending the correct data
structure:

JSON

{

\"id\": \"40\",

\"title\": \"Think\", // Correct field was being ignored by UI

\"company\": {

\"name\": \"Doggo Life\", // This was being used as the Title

},

\"score\": 4.46

}

### **3. Important Code Snippets**

#### **❌ The Buggy Code (Search.tsx):**

TypeScript

// Inside JobsSection component

\<View style={styles.listItemInfo}\>

{/\* BUG: Rendering company name as the main title \*/}

\<Text style={styles.listItemTitle}\>{item.company.name}\</Text\>

{/\* BUG: Hardcoded subtitle text \*/}

\<Text style={styles.listItemSubtitle}\>Fintech\</Text\>

\</View\>

#### **✅ The Solution Code (Search.tsx):**

TypeScript

// Corrected Mapping

\<View style={styles.listItemInfo}\>

{/\* Corrected: Show the actual Job Title (e.g., \"Think\") \*/}

\<Text style={styles.listItemTitle}\>{item.title}\</Text\>

{/\* Corrected: Show the Company Name as the subtitle \*/}

\<Text style={styles.listItemSubtitle}\>{item.company.name}\</Text\>

\</View\>

### **4. Files Involved**

  ---------------------------------------------------------------------------
  **File Path**                            **Role**
  ---------------------------------------- ----------------------------------
  src/screens/search/Search.tsx            **Main File:** Contained the
                                           faulty rendering logic in the
                                           JobsSection component.

  src/screens/search/searchStyes.ts        **Styles:** Provided the
                                           listItemTitle and listItemSubtitle
                                           formatting.

  src/screens/home/JobOpportunities.tsx    **Reference:** Used for verifying
                                           the consistent data structure used
                                           on the Dashboard.

  src/screens/job_portal/JobPostings.tsx   **Reference:** Used for verifying
                                           the full job list data structure.
  ---------------------------------------------------------------------------

### **5. Solution Overview**

The fix involved remapping the data fields within the JobsSection
component in Search.tsx. By swapping item.company.name for item.title in
the primary \<Text\> component and replacing the hardcoded \"Fintech\"
string with the dynamic company name, the UI now accurately reflects the
search results while maintaining the original design and theme styles.

> **Note for Future Reference:** Always verify the data mapping in
> Search sub-sections (PeopleSection, CompaniesSection, JobsSection)
> when adding new search scopes to ensure the API\'s returned object
> properties align with the component\'s item accessors.

# Problem 82

Here is a summary of the initial problem, root cause, and solution for
removing the global \"CHIIRO\" loader from your Search screen for your
future reference.

### **The Problem**

When navigating to the Search screen, a global full-screen \"CHIIRO\"
loader (LoaderAnimation.tsx) was appearing instead of the intended
screen-specific loading UI.

### **The Root Cause**

The issue was not inside the main Search.tsx logic. Instead, the Search
screen was being lazily loaded via React.lazy inside its index file.
While the app was fetching the code chunk for the Search screen,
React\'s \<Suspense\> boundary was triggering its fallback UI. In this
case, the fallback was set to a shared \<Fallback /\> component, which
rendered the global CHIIRO loader.

### **The Solution**

To disable the global loader specifically for this route without
breaking other screens, the \<Fallback /\> component was removed from
the Suspense boundary in the Search screen\'s index file and replaced
with null. This allowed the screen to load silently and pass the loading
responsibility to the internal skeletons (SearchScreenSkeleton and
ListItemSkeleton) defined inside Search.tsx.

### **Reference Code**

**File:** src/screens/search/index.tsx

**Before (Causing the issue):**

TypeScript

import React from \'react\';

import Fallback from \'@/components/common/Fallback\';

const SearchScreen = React.lazy(() =\> import(\'./Search\'));

export const SearchScreenPage = (props: any) =\> (

\<React.Suspense fallback={\<Fallback /\>}\>

\<SearchScreen {\...props} /\>

\</React.Suspense\>

);

**After (The Fix):**

TypeScript

import React from \'react\';

const SearchScreen = React.lazy(() =\> import(\'./Search\'));

export const SearchScreenPage = (props: any) =\> (

\<React.Suspense fallback={null}\>

\<SearchScreen {\...props} /\>

\</React.Suspense\>

);

# Problem 83

You've effectively bridged the gap between a generic \"Join\" button and
a specialized **Moderation Flow** for private communities. By utilizing
the pending state returned by your backend, you've ensured that the UI
remains in sync with the user\'s actual membership status.

Here is the breakdown of your implementation for future reference.

## **🛠 Feature Summary: User-Side Join Flow**

You implemented a multi-stage interaction for communities where privacy
=== \'private\' and join_policy === \'request\':

1.  **Trigger:** User clicks \"Join Community\" or \"Send Request.\"

2.  **Consent:** A RulesAgreementModal is triggered.

3.  **Action:** Upon agreement, a POST request is sent to the join
    endpoint.

4.  **State Change:** The UI immediately reflects a \"Pending\" state,
    disabling the button and changing the label to \"Request Sent\" to
    prevent duplicate requests.

## **📂 Files Modified**

- **CommunityDetail.tsx**: The primary screen where all conditional
  logic for the community header, join buttons, and content locking
  resides.

- **RulesAgreementModal.tsx**: (Referenced) The shared component that
  handles rule display and the confirmation callback.

## **📝 Key Code Snippets**

### **1. State Extraction**

You extracted the specific membership status from the communityInfo
object to drive the UI.

TypeScript

const membershipStatus = pathOr(\'none\', \[\'membership\',
\'status\'\], communityInfo);

const isPending = membershipStatus === \'pending\';

### **2. Dynamic Button Logic**

You updated the professional join button to handle the three primary
states: **Joined**, **Pending**, and **Stranger**.

TypeScript

\<TouchableOpacity

style={\[

styles.professionalJoinButton,

isJoined && styles.professionalJoinedButton,

\]}

// Logic: Only allow pressing if not already joined or pending

onPress={isJoined ? handleLeaveToggle : isPending ? undefined :
handleJoinToggle}

disabled={isJoinPending \|\| isLeavePending \|\| isPending}

\>

{/\* Icon Switching \*/}

\<Icon

source={isJoined ? \'logout\' : isPending ? \'clock-outline\' :
\'plus\'}

size={20}

color={isJoined ? \'#FA0000\' : theme.colors.buttonText}

/\>

{/\* Text Switching \*/}

\<Text style={styles.professionalJoinButtonText}\>

{isJoined

? \'Leave Community\'

: isPending

? \'Request Sent\'

: privacySetting === \'private\'

? \'Send Request\'

: \'Join Community\'}

\</Text\>

\</TouchableOpacity\>

## **📡 Endpoint & Data Availability**

Your debugging process confirmed that the backend is fully supportive of
this flow.

  ------------------------------------------------------------------------------------
  **Endpoint**                      **Method**   **Purpose**         **Data Status**
  --------------------------------- ------------ ------------------- -----------------
  /communities/{id}                 GET          Fetch community     **Available:**
                                                 details &           Returns status:
                                                 membership status.  \"pending\" after
                                                                     join.

  /community-membership/{id}/join   POST         Initiates the join  **Available:**
                                                 request.            Returns 201
                                                                     Created.

  /communities/{id}/rules           GET          Fetches rules for   **Available:**
                                                 the modal.          Accessible even
                                                                     if status is
                                                                     none.
  ------------------------------------------------------------------------------------

> \[!IMPORTANT\]
>
> **Data Verification:** Your logs confirmed that after calling the join
> endpoint, a subsequent refresh of the community data successfully
> updates membership.status from \"none\" to \"pending\". This is the
> single most important piece of data for your UI logic.

Since you\'ve already designed the **Admin/Invitation** side in the
Notifications screen, are the \"Approve\" and \"Ignore\" mutations
already defined in your useCommunity hooks, or do we need to check the
API for those next?

# Problem 84

Here is the rewritten summary, perfectly aligned with the exact
technical steps and logic we used to resolve the issue:

### **Problem Summary**

We needed to implement Edit and Delete functionality for comments to
match the existing design and logic of the AnswerCard component. The
primary blockers were:

1.  **Ownership Logic Failure:** The backend API for comments was not
    returning an is_owner flag, causing the application to falsely
    assume the logged-in user did not own their comments, which hid the
    action buttons.

2.  **UI Layout Inconsistency:** The buttons were wrapped in an isolated
    \<View\> container, preventing them from aligning correctly within
    the main action bar.

### **Key Files Referenced**

  -------------------------------------------------------------------------
  **File Name**                                             **Purpose**
  --------------------------------------------------------- ---------------
  src/screens/community/components/common/CommnetCard.tsx   The primary UI
                                                            component where
                                                            the ownership
                                                            logic and
                                                            button layouts
                                                            were updated.

  src/store/authStore.ts                                    The Zustand
                                                            store imported
                                                            to retrieve the
                                                            currently
                                                            authenticated
                                                            user\'s ID for
                                                            frontend
                                                            ownership
                                                            validation.
  -------------------------------------------------------------------------

### **The Solution**

#### **1. Robust Ownership Verification (Frontend Fallback)**

To bypass the missing API flag without breaking backward compatibility,
we implemented a fallback mechanism. We imported useAuthStore to
calculate ownership directly on the frontend. By comparing the active
user\'s ID with the comment author\'s ID---and wrapping both in a
String() constructor---we prevented potential type-mismatch bugs (e.g.,
comparing a string ID to a number ID).

TypeScript

// Inside CommnetCard.tsx

import { useAuthStore } from \'@/store/authStore\';

// \... inside the component

const { user } = useAuthStore();

// Check backend flags first, then fallback to string-safe frontend ID
comparison

const isBackendOwner = pathOr(false, \[\'is_owner\'\], comment) \|\|
pathOr(false, \[\'user\', \'is_owner\'\], comment);

const isFrontendOwner = Boolean(user?.id && comment?.user?.id &&
String(user.id) === String(comment.user.id));

const currentUserComment = isBackendOwner \|\| isFrontendOwner;

#### **2. UI Layout Alignment**

To perfectly mirror the AnswerCard design, we removed the parent wrapper
(\<View style={{ flexDirection: \'row\', marginLeft: \'auto\' }}\>) that
was previously housing the icons. We placed the conditionally rendered
IconButton components directly inside the actionBar View so they sit
horizontally next to the vote buttons, cleanly inheriting the existing
gap: theme.spacing.lg styling.

TypeScript

\<View style={styles.actionBar}\>

{/\* \... Upvote/Downvote buttons \... \*/}

{/\* EDIT \*/}

{currentUserComment && (

\<IconButton

icon={\'square-edit-outline\'}

size={theme.fonts.sizes.lg}

iconColor={theme.colors.textSecondary}

style={styles.iconButton}

loading={updateCommentsPending}

onPress={() =\> setIsUpdateVisible(true)}

/\>

)}

{/\* DELETE \*/}

{currentUserComment && (

\<IconButton

icon={\'delete\'}

size={theme.fonts.sizes.lg}

iconColor={theme.colors.error}

style={styles.iconButton}

loading={deleteCommentsLoading}

onPress={() =\> setIsDeleteVisible(true)}

/\>

)}

\</View\>

**Outcome:** Everything is now integrated according to the project\'s
existing structure. The implementation strictly follows the principle of
backward compatibility: if the backend is later updated to return
is_owner, the component will seamlessly prioritize the backend flag
without requiring further code changes.

# Problem 85

Here is a technical summary of the task and the solution implemented to
hide the red \"Leave Community\" button while adhering to your project
constraints.

## **📋 Task Summary: Hiding the \"Leave Community\" Button**

### **🔍 The Problem**

The user profile screen displays a list of joined communities. Each
community item rendered via a shared CommunityCard component included a
red \"logout\" icon. The goal was to remove or hide this specific button
on the **Profile screen** without affecting the button\'s visibility in
other parts of the application (e.g., a \"My Communities\" management
screen).

### **📂 File Reference**

  -----------------------------------------------------------------------------
  **File Path**                                        **Role**
  ---------------------------------------------------- ------------------------
  src/screens/profile/CommunityTab.tsx                 **Target File.** The
                                                       parent container that
                                                       manages the list logic
                                                       for the profile.

  src/components/common/CommunityCard.tsx              **Shared Component.**
                                                       Contains the UI for the
                                                       red button; left
                                                       untouched to ensure
                                                       backward compatibility.

  src/screens/profile/components/UserProfileCard.tsx   **Header Component.**
                                                       Handles the top profile
                                                       info (Avatar, Stats);
                                                       unrelated to the
                                                       community list.
  -----------------------------------------------------------------------------

### **🛠️ The Solution**

To satisfy the **Golden Rule of Backward Compatibility**, we avoided
deleting the button code inside the shared CommunityCard.tsx. Instead,
we modified the **caller logic** in CommunityTab.tsx.

By passing showLeaveOption={false} to the card, the button is hidden
only on this specific screen. This ensures that if the CommunityCard is
used elsewhere where leaving a community is a required feature, the
logic remains intact.

### **💻 Important Code Snippets**

#### **1. The Trigger (In CommunityCard.tsx)**

This is the code block that renders the button based on the
showLeaveOption prop:

TypeScript

{showLeaveOption && onLeave && (

\<IconButton

icon=\"logout\"

size={20}

iconColor={\'red\'}

onPress={handleLeavePress}

/\>

)}

#### **2. The Implementation (In CommunityTab.tsx)**

We updated the renderItem function in the FlatList to explicitly disable
this option:

**Before:**

TypeScript

showLeaveOption={isOwner} // Button showed if the user was the profile
owner

**After (Fixed):**

TypeScript

\<CommunityCard

community={item}

styles={styles}

handleNavigationCommunity={handleNavigationCommunity}

showLeaveOption={false} // \<\-\-- Hardcoded to false to hide the button

showIsMutual={isOwner ? false : true}

onLeave={handleLeaveCommunity}

/\>

### **✅ Constraints Check**

- **Backward Compatibility:** Maintained. The shared component still
  supports the leave functionality for other screens.

- **Logic Preservation:** The handleLeaveCommunity function was not
  removed, allowing for easy restoration if requirements change.

- **Style Integrity:** No CSS or global styles were altered; we only
  toggled a boolean prop.

# Problem 86

## **Problem Summary**

The **Education form** (School name, Degree, Field of Study) was showing
\"No options found\" when the selection modal was first opened. In
contrast, the **Experience form** (Company name) would immediately
populate with a list of options.

### **The Root Cause**

The issue was located in the **API hooks logic**. The hooks used for the
Education form had a strict requirement that the search query must not
be empty (enabled: isEmpty(query) === false) before triggering the API
call. The hooks for the Experience form had this requirement commented
out, allowing them to fetch a default list of options as soon as the
modal opened.

## **File: src/api/hooks/useAutoCompleted.ts**

### **❌ The Problematic Code**

The enabled property was preventing the API from fetching data when the
user first clicked the field (since the search text is initially empty).

TypeScript

// Example of the restricted hook

export const useAutoEducations = (query: string) =\> {

return useQuery({

queryKey: \[queryKeys.autoComplete.education, query\],

queryFn: () =\> Educations(query),

enabled: isEmpty(query) === false, // ❗ This line was blocking initial
data

});

};

### **✅ The Solution**

Comment out or remove the enabled constraint to allow the field to fetch
\"initial\" or \"trending\" results immediately upon opening the modal.

TypeScript

export const useAutoEducations = (query: string) =\> {

return useQuery({

queryKey: \[queryKeys.autoComplete.education, query\],

queryFn: () =\> Educations(query),

// enabled: isEmpty(query) === false, // ✅ Commented out to match
ExperienceForm behavior

});

};

export const useAutoDegree = (query: string) =\> {

return useQuery({

queryKey: \[queryKeys.autoComplete.degree, query\],

queryFn: () =\> Degree(query),

// enabled: isEmpty(query) === false,

});

};

export const useAutoFieldOfStudy = (query: string) =\> {

return useQuery({

queryKey: \[queryKeys.autoComplete.fieldOfStudy, query\],

queryFn: () =\> FieldOfStudy(query),

// enabled: isEmpty(query) === false,

});

};

## **Important File References**

  ---------------------------------------------------------------------------
  **File Name**                **Role in Problem**
  ---------------------------- ----------------------------------------------
  **EducationForm.tsx**        Defined the fields with searchType:
                               \'school\', \'degree\', and \'fieldOfStudy\'.

  **AutocompleteField.tsx**    The shared UI component that manages the
                               search modal and calls the API hooks.

  **useAutoCompleted.ts**      **(The Fix Location)** Contains the TanStack
                               Query hooks that control when API calls are
                               triggered.

  **autcomplete.service.ts**   The underlying service that makes the actual
                               Axios/Fetch calls to the backend.
  ---------------------------------------------------------------------------

## **Future Reference Note**

When creating new autocomplete fields in the future:

1.  **If you want initial data on click:** Ensure enabled is either not
    defined or set to true.

2.  **If you want to save API calls (Search only):** Keep enabled:
    query.length \> 0 or similar logic.

# Problem 87

#Enabling Screen Recording for Login Flow

I have modified the native Android code to prevent the login screen (and
the rest of the app) from being blacked out during screen recordings or
when using screenshots.

\## Changes Made

\### Android Native

\####
\[MainActivity.kt\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/android/app/src/main/java/com/chiiro/app/MainActivity.kt)

I updated the \`MainActivity\` to explicitly clear the \`FLAG_SECURE\`
flag during the \`onCreate\` lifecycle method. This flag is the primary
reason why Android screens appear black in recordings.

\`\`\`kotlin

override fun onCreate(savedInstanceState: Bundle?) {

super.onCreate(null)

window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)

}

\`\`\`

\## How to Verify

1\. \*\*Rebuild the App\*\*: Since this is a native change, you need to
rebuild the Android application:

\`\`\`bash

yarn android

\`\`\`

2\. \*\*Navigate to Login\*\*: Go to the login screen where you
previously experienced the black screen.

3\. \*\*Start Screen Recording\*\*: Use your phone\'s built-in screen
recorder or a third-party app.

4\. \*\*Confirm Visibility\*\*: The login screen should now be correctly
captured in the recording, allowing you to record the entire user flow.

\> \[!NOTE\]

\> Clearing this flag also allows the app to be visible in the \"App
Switcher\" (Recents) view instead of showing a black rectangle.

\> \[!WARNING\]

\> While this allows you to record the flow, it technically reduces the
security of the login screen by allowing other apps (if they have screen
capture permissions) to potentially see the login fields. It is
recommended to keep this for your recording session and consider the
security implications for production releases.

# Problem 88

This report summarizes the implementation of the **Development Helpers
and OTP Bypass** for the CHIIRO React Native project. This system was
designed to eliminate the friction of manual data entry and backend OTP
dependencies during the development phase.

## **Project Report: Registration Flow Development Helpers**

### **1. Objective**

To streamline end-to-end testing of the registration and onboarding flow
by:

- Automating form entry with unique dummy data.

- Bypassing the backend OTP verification requirement using a \"Magic
  Code\" and specific email domain.

- Ensuring authentication state persists even when the server-side
  verification is skipped.

### **2. Key File Changes & Code Snippets**

#### **File 1: RegistrationScreen.tsx**

**Location:** src/screens/founder/auth/RegistrationScreen.tsx

- **Logic Implementation:** Added a handleDevAutofill function that uses
  react-hook-form\'s setValue to populate state.

- **Auth Persistence:** Updated the registration onSuccess handler to
  save the user object to the authStore immediately.

**Important Snippet (UI):**

TypeScript

{/\* Placed before the social login section \*/}

{\_\_DEV\_\_ && (

\<TouchableOpacity

onPress={handleDevAutofill}

style={styles.devButton}

\>

\<Text style={styles.devText}\>DEBUG: Fill Dummy Data\</Text\>

\</TouchableOpacity\>

)}

#### **File 2: OtpScreen.tsx**

**Location:** src/screens/founder/auth/OtpScreen.tsx

- **Bypass Logic:** Intercepts the Continue button press. If the
  conditions match, it navigates to the next screen without calling the
  /auth/verify-otp API.

- **OTP Helper:** A button to quickly set the state to the \"Magic
  Code.\"

**Important Snippet (Bypass Logic):**

TypeScript

const handleContinue = () =\> {

const isDummyUser = email.endsWith(\'@example.com\') && otp ===
\'123456\';

if (\_\_DEV\_\_ && isDummyUser) {

// Skip API call and trigger success navigation

navigation.navigate(\'RoleSelection\');

return;

}

// Standard API call logic follows\...

};

### **3. Verification Path (The \"Happy Path\")**

1.  **Start:** Open Registration Screen in a \_\_DEV\_\_ environment.

2.  **Autofill:** Tap **\"DEBUG: Fill Dummy Data\"** (Generates unique
    email: testuser\_\[timestamp\]@example.com).

3.  **Submit:** Click **\"Register\"**.

4.  **Bypass:** On the OTP screen, tap **\"DEBUG: Fill OTP (123456)\"**.

5.  **Finish:** Click **\"Continue\"**. The app transitions to **Role
    Selection** without a backend error.

### **4. Future Removal & Cleanup Guide**

When the project is ready for staging or production, you will need to
remove these helpers to maintain security. Follow these steps:

#### **Step A: Search and Destroy \_\_DEV\_\_ Blocks**

Search the codebase for the {\_\_DEV\_\_ && \...} pattern specifically
within RegistrationScreen.tsx and OtpScreen.tsx.

- **Remove:** The TouchableOpacity components for \"Fill Dummy Data\"
  and \"Fill OTP.\"

- **Remove:** The handleDevAutofill function definition.

#### **Step B: Revert the OTP Handler**

In OtpScreen.tsx, remove the isDummyUser check inside the handleContinue
function. Ensure the function only contains the actual API mutation
logic.

#### **Step C: Audit the authStore Update**

Check if saving the user object in the RegistrationScreen success
handler is still desired.

- **Normal Flow:** Usually, the user object and token are saved *only
  after* a successful OTP verification.

- **Reversion:** You may need to move the authStore.setUser() logic back
  into the OtpScreen success handler.

> \[!TIP\]
>
> **Pro-Tip for Future Victor:** Because these are wrapped in
> \_\_DEV\_\_, they will **automatically be excluded** from the final
> production bundle by the React Native compiler. However, removing the
> code manually is still best practice to keep the codebase clean and
> prevent \"Dead Code\" accumulation.

# Problem 89

I couldn\'t see the job title, icon, date, type of job,location and was
only able to see the apply button in the Job Opportunities section in
the Home Screen of the app.

I found the root cause of the issue and have already applied the fix!

\### \*\*What was the Reason?\*\*

The \`\<Button\>\` component in \`src/components/common/Button.tsx\` was
recently refactored to include an inner wrapper \`\<View\>\` styled with
\`width: \'100%\'\` (to ensure the text and loaders inside it stay
centered and stretch evenly).

However, in \`src/components/home/JobOpportunities.tsx\`, the layout
relies on a \`flexDirection: \"row\"\` approach, where the left-hand
text content (\`contentContainer\`) has \`flex: 1\` and uses the
remaining space next to the right-hand container holding the button.
Because the \`Button\` was aggressively requesting 100% width, it
forcefully expanded to the size of the entire card parent. This
completely consumed all available horizontal space, compressing
\`contentContainer\` to zero width (those two faint, vertical slivers of
color visible in your screenshot below the button are actually the tags,
completely squished vertically!) and making it seem like all content
disappeared.

\### \*\*How it was Fixed:\*\*

1\. \*\*Made Button \`width\` Configurable
(\`src/components/common/Button.tsx\`)\*\*

I updated the \`\<Button\>\` component to accept an optional
\`fullWidth\` prop. To comply with the backward compatibility rule,
\`fullWidth\` defaults to \`true\` so no other screens relying on it
break.

\`\`\`tsx

export const Button: React.FC\<ButtonProps\> = ({

title,

// \...

fullWidth = true, // Ensures it behaves as it used to natively

}) =\> {

// \...

\<View style={{ \... (fullWidth ? { width: \'100%\' } : {}) }}\>

\`\`\`

2\. \*\*Provided Prop to the Card
(\`src/components/home/JobOpportunities.tsx\`)\*\*

I passed \`fullWidth={false}\` to the \`Button\` instance inside the
\`JobOpportunities\` card. This restores the proper \`flex: 1\`
tug-of-war for horizontal space between the job details and the button
itself.

The UI in the Job Opportunities component will now render the text
content, icons, metadata, and tags accurately side-by-side with the
\"Apply\" button!

# Problem 90

VirtualizedLists should never be nested inside plain ScrollViews with
the same orientation because it can break windowing and other
functionality - use another VirtualizedList-backed container instead.

when in Home Screen after clicking a card in the Recommended Communities
section, i was sent to the community detail page, where i was shown this
VirtualizedLists error.

\### Why was this error happening?

React Native\'s \`ScrollView\` renders all of its children at once so
you can scroll through them. A \`FlatList\` (which is a type of
\`VirtualizedList\`), on the other hand, is specifically optimized to
only render children that are currently visible on the screen to save
memory (a process called \"windowing\").

When you place a vertical \`FlatList\` directly inside a vertical
\`ScrollView\`, the \`ScrollView\` forcefully expands the \`FlatList\`
to its full, unbounded height. Because the \`FlatList\` now thinks it\'s
fully visible at all times, it renders \*all\* of its items
simultaneously, entirely defeating its underlying performance
optimizations. React Native detects this layout flaw and throws the
warning you saw to prevent you from unknowingly breaking the list\'s
windowing functionality.

\### Where was it coming from?

The error was originating from
\`src/screens/community/components/community-detail/Members.tsx\`. The
\`Members\` component was using a \`FlatList\` to render the list of
community members and admins.

However, over in \`src/screens/community/CommunityDetail.tsx\`, the tab
container (and subsequently the \`Members\` component inside the tabs)
itself is wrapped inside a massive top-level \`ScrollView\`. This is
what created the nested \`ScrollView\` \> \`FlatList\` clash.

\*(Note: The \`RecommendedCommunities.tsx\` file you supplied \*does\*
use a \`FlatList\`, but because it scrolls \`horizontally\`, it doesn\'t
conflict with a vertical \`ScrollView\`. Only lists with the
\*\*same\*\* orientation collision cause this precise error.)\*

\### How it was solved

I modified the \`Members.tsx\` component. Instead of using a
\`FlatList\` which conflicts with the parent, I changed it to a normal
\`View\` container that simply maps through the \`members\` array using
a standard \`.map()\` function.

This safely works with the parent \`CommunityDetail\`\'s \`ScrollView\`,
correctly rendering your members list while fully eliminating the
\"VirtualizedLists should never be nested inside plain ScrollViews\"
error.

# Problem 91

Console Error

❌ API Error: {\"status\":403,
\"url\":\"discussions/communities/373/list\", \"message\":\"Request
failed with status code 403\", \"data\":{\"success\":false,
\"message\":\"You must be a member of this private community to access
its content\", \"statusCode\":403,
\"timestamp\":\"2026-04-17T05:13:22.983Z\"}}

When I clicked on the One Piece community(private community) which is a
part of the Recommended Communities section, it sent me to the community
detail page.

there i got the above error:

\*\*Is this error intended?\*\*

Yes and no. The server returning a \`403 Forbidden\` response is fully
intended because the backend enforces privacy rules blocking non-members
from accessing a private community\'s posts. However, the app fetching
the API \*before\* verifying if the community is locked and subsequently
triggering a global error toast was an unintended client-side behavior.

\*\*How to remove it?\*\*

Since \`CommunityDetail\` was attempting to fetch both the
\`communityInfo\` and the \`postsData\` in parallel immediately upon
rendering, it hit the blocked endpoint right away. To fix this, I made
the query execution conditional so the posts fetch is skipped if you
aren\'t permitted to view them.

Here are the changes I made to resolve this:

1\. \*\*Updated \`usePostInCommunity\` Hook:\*\*

\- Modified \`src/api/hooks/useDiscussion.ts\` to accept an \`options\`
parameter containing an \`enabled\` flag, similar to typical
\`react-query\` hooks. This backward-compatible change controls when the
query attempts to fetch data.

2\. \*\*Added Locked States in \`CommunityDetail.tsx\`:\*\*

\- Disabled \`usePostInCommunity\` from fetching if \`isInitialLoading\`
is true (before we know the community type) or if \`isLocked\` evaluates
to true (private and user is not a member or owner).

\- Modified the pull-to-refresh (\`onRefresh\`) handler to ensure
\`refetchPosts()\` is only triggered when \`!isLocked\`.

This fix will cleanly prevent the \`403\` log and toast error, allowing
your UI (with the lock icon) to handle the visual representation
gracefully!

Below are the code changes i made to fix this error:

## **1. src/api/hooks/useDiscussion.ts**

### **Removed:**

TypeScript

export const usePostInCommunity = (communityId: string \| number) =\>

useQuery({

queryKey: \[queryKeys.discussion.postListInCommunity, communityId\],

queryFn: () =\> PostListInCommunity(communityId),

enabled: !!communityId,

### **Added:**

TypeScript

export const usePostInCommunity = (communityId: string \| number,
options?: { enabled?: boolean }) =\>

useQuery({

queryKey: \[queryKeys.discussion.postListInCommunity, communityId\],

queryFn: () =\> PostListInCommunity(communityId),

enabled: options?.enabled !== undefined ? !!communityId &&
options.enabled : !!communityId,

## **2. src/screens/community/CommunityDetail.tsx**

### **Part A: Hook Call and Logical Order**

**Removed:**

*(The hook was called before the community state was calculated)*

TypeScript

} = usePostInCommunity(communityId);

const communityInfo = pathOr({}, \[\'data\'\], fetchedCommunityData);

const isJoined = pathOr(false, \[\'membership\', \'is_member\'\],
communityInfo);

const isOwner = (pathOr(\'\', \[\'membership\', \'role\'\],
communityInfo) as string) === \'owner\';

const isPrivate = pathOr(\'public\', \[\'privacy\'\],
communityInfo).toLowerCase() !== \'public\';

const isLocked = isPrivate && !isJoined && !isOwner;

**Added:**

*(Hoisted the variables and passed the enabled flag to the hook)*

TypeScript

const communityInfo = pathOr({}, \[\'data\'\], fetchedCommunityData);

const isInitialLoading = Object.keys(communityInfo).length === 0;

const isJoined = pathOr(false, \[\'membership\', \'is_member\'\],
communityInfo);

const isOwner = (pathOr(\'\', \[\'membership\', \'role\'\],
communityInfo) as string) === \'owner\';

const isPrivate = pathOr(\'public\', \[\'privacy\'\],
communityInfo).toLowerCase() !== \'public\';

const isLocked = isPrivate && !isJoined && !isOwner;

} = usePostInCommunity(communityId, { enabled: isInitialLoading ? false
: !isLocked });

### **Part B: Pull-to-Refresh Guard**

**Removed:**

TypeScript

onRefresh={() =\> {

refetch();

refetchPosts();

}}

**Added:**

TypeScript

onRefresh={() =\> {

refetch();

if (!isLocked) {

refetchPosts();

}

}}

# Problem 92

Users navigating to a profile (e.g., clicking a name in the Feed tab)
were staying within the \"Persistent Shell\" of the bottom tab
navigator. This caused two main issues:

\- \*\*UI Inconsistency\*\*: Unlike other detail screens (like
\`CommunityDetail\`), the bottom tab bar remained visible, which was not
the intended UX for profile details.

\- \*\*Incorrect Back Navigation\*\*: Pressing the back arrow at the top
often returned the user to the \*\*Home\*\* tab instead of the specific
screen they started from (e.g., the \*\*Feed\*\* tab within the
Community dashboard). This happened because the profile was being
treated as a \"hidden tab\" switch rather than a stack push.

\## The Solution

The root cause was \"Route Duplication\" across different levels of the
navigation hierarchy. The \`UserProfile\` route existed both in the
\*\*App Navigator\*\* (Root Stack) and the \*\*Main Navigator\*\*
(Bottom Tabs).

\### Modifications:

\- \*\*Removed Duplicate Routes\*\*: The \`SCREEN_NAMES.USER_PROFILE\`
screen was removed from the \`Tab.Navigator\` blocks in both
\`MainNavigator\` and \`MainInvestorNavigator\`.

\- \*\*Forced Stack Bubbling\*\*: By removing the screen from the nested
tab navigator, any call to \`navigation.navigate(\'UserProfile\')\` now
automatically \"bubbles up\" to the parent Root Stack. This forces the
profile to be pushed as a standard stack screen.

\## Files Involved

\-
\*\*\[MainNavigator.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/navigation/MainNavigator.tsx)\*\*:
Removed \`\<Tab.Screen name={SCREEN_NAMES.USER_PROFILE} \... /\>\`
blocks from the hidden tabs section.

\-
\*\*\[AppNavigator.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/navigation/AppNavigator.tsx)\*\*:
(Verified) This file already contained the stack definition for
\`USER_PROFILE\`, which now handles all profile navigation.

\## Best Practices for Navigation

Following these principles will help avoid similar issues in the future:

\### avoid Route Duplication

Never define the same screen name in two different navigators unless you
specifically intend to have two different instances of that screen with
different behaviors. React Navigation prioritizes the closest navigator,
which can lead to unexpected \"Persistent Shell\" behavior.

\### Use Stack Pushes for Detail Screens

Screens that represent a deep dive into an entity (User, Community,
Post) should generally be part of a \*\*Stack Navigator\*\* sitting
ABOVE the \*\*Bottom Tab Navigator\*\*. This ensures:

1\. The bottom tabs are hidden to give more focus to the content.

2\. The standard navigation stack behavior (\`goBack()\`) works
predictably across all platforms.

\### Understand Navigation Bubbling

When \`navigation.navigate(\'ScreenName\')\` is called, React Navigation
searches the current navigator. if not found, it asks the parent, and so
on. Use this to your advantage to trigger stack pushes from within tab
contexts.

\### Consistent Header Behavior

Always use a uniform Header component (like \`TopHeader\`) that relies
on \`navigation.goBack()\`. This ensures that as long as your stack
hierarchy is correct, the back button will always function intuitively.

\-\--

\> \[!TIP\]

\> If you ever want a screen to keep the bottom tabs visible, add it as
a hidden tab in \`MainNavigator\`. If you want it to behave like a
standard full-screen detail page, keep it in \`AppNavigator\` only.

# Problem 93

Blank/Grey screen with text 'downloading'

This report provides a definitive architectural pattern for eliminating
navigation flickers in React Native apps using code-splitting
(React.lazy). It addresses the \"Lifecycle Gap\" that causes the dreaded
grey \"Downloading\...\" screen.

## **1. The Diagnosis: The Dual-Phase Loading Gap**

When a screen is lazy-loaded, the transition happens in two distinct
phases. Most performance issues occur because developers only optimize
for the second phase.

  -----------------------------------------------------------------------------
  **Phase**   **Technical State**   **The Visual          **The \"Problem 93\"
                                    Symptom**             Error**
  ----------- --------------------- --------------------- ---------------------
  **Phase 1:  React.lazy is         **Grey/Blank Screen** The skeleton was
  The Chunk   fetching the JS       with                  *inside* the file
  Load**      bundle.               \"Downloading\...\"   being downloaded, so
                                    text.                 it was inaccessible.

  **Phase 2:  JS is loaded; Screen  **Stuttering          InteractionManager
  The         is                    Animation** or layout was used, but the
  Render**    mounting/animating.   jumps.                \"Phase 1\" flicker
                                                          already ruined the
                                                          UX.
  -----------------------------------------------------------------------------

## **2. The Solution: Two-Tier Defense Architecture**

To achieve a \"Zero-Flicker\" transition, the loading UI must be hoisted
**above** the lazy-loaded component.

### **Tier 1: The Wrapper Defense (Fixes Phase 1)**

**File:** src/screens/chat_bot/index.tsx

This is the most critical change. The fallback UI must be defined in the
entry point file. This ensures the skeleton is part of the \"Main
Bundle\" and can render **instantly** without waiting for the ChatBot
chunk.

TypeScript

// index.tsx - THE WRAPPER

const ChatBotScreen = React.lazy(() =\> import(\'./ChatBotScreen\'));

const ChatBotPage = (props: any) =\> {

const theme = useTheme();

return (

\<React.Suspense

fallback={

/\* This renders IMMEDIATELY upon button click \*/

\<View style={{ flex: 1, backgroundColor: theme.isDark ? \'#1A1A1A\' :
\'#FAFAFA\' }}\>

\<TopHeader title=\"Co-founder & Partner Search\" /\>

\<AiChatBotSekeletonLoader /\>

\</View\>

}

\>

\<ChatBotScreen {\...props} /\>

\</React.Suspense\>

);

};

### **Tier 2: The Transition Guard (Fixes Phase 2)**

**File:** src/screens/chat_bot/ChatBotScreen.tsx

Once the code is downloaded, we prevent the \"Heavy Render\" from
choking the navigation animation.

TypeScript

// ChatBotScreen.tsx - THE SCREEN

const \[isTransitionReady, setIsTransitionReady\] = useState(false);

useEffect(() =\> {

// Wait for the slide-in animation to finish 100%

const task = InteractionManager.runAfterInteractions(() =\> {

setIsTransitionReady(true);

});

return () =\> task.cancel();

}, \[\]);

// COMBINED LOGIC: Stay in skeleton mode until animation is done OR data
is loading

const shouldShowSkeleton = !isTransitionReady \|\| (isLoading &&
messages.length === 0);

if (shouldShowSkeleton) {

return (

\<View style={{ flex: 1, backgroundColor: theme.isDark ? \'#1A1A1A\' :
\'#FAFAFA\' }}\>

\<TopHeader title=\"Co-founder & Partner Search\" /\>

\<AiChatBotSekeletonLoader /\>

\</View\>

);

}

## **3. Why This Worked (The Insight)**

The \"Problem 93\" approach failed because the **Skeleton was a prisoner
of the lazy-load.** By moving the AiChatBotSekeletonLoader into the
Suspense fallback in index.tsx, you essentially \"leak\" the loading UI
into the main app bundle. This allows the app to show the skeleton
**before it even starts downloading the screen\'s code.** 1. **Click AI
Button** → Suspense sees code isn\'t ready → Shows fallback (Skeleton)
**instantly**.

2\. **Chunk Downloads** in the background.

3\. **Chunk Finishes** → ChatBotScreen mounts → It also shows the
Skeleton (via shouldShowSkeleton).

4\. **Animation Finishes** → InteractionManager fires → Skeleton
disappears, Chat UI appears.

## **4. Best Practices for Other \"Heavy\" Screens**

Whenever you encounter a \"Grey Flicker\" on a new screen, apply this
checklist:

1.  **Hoisted Fallbacks:** Is the Suspense fallback in the index.tsx
    wrapper? (It should be).

2.  **Asset Mirroring:** Does the fallback UI use the exact same
    TopHeader and background hex code as the final screen? (Prevents
    \"micro-flickers\").

3.  **Skeleton Stability:** Does the skeleton loader occupy the same
    vertical space as the final content? (Prevents \"Layout Jumps\").

4.  **Interaction Guard:** Are you using InteractionManager to delay
    rendering of heavy components like Markdown, FlatLists, or Video?

### **Summary of Component Roles**

- **index.tsx**: Responsible for the **Loading State** (User Perception
  of Speed).

- **ChatBotScreen.tsx**: Responsible for the **Execution State** (User
  Perception of Smoothness).

# Problem 94

\# Report: Eliminating Home Screen Navigation Flicker(blank/grey screen)

\## 1. Problem Description

Users experienced a three-phase visual flicker when navigating to the
Home screen after a successful login:

1\. \*\*Initial Phase:\*\* The \`HomeScreenSkeletonLoader\` appeared
briefly.

2\. \*\*Intermediate Phase:\*\* A \*\*grey screen\*\* (bare background)
appeared for \~400-800ms.

3\. \*\*Final Phase:\*\* The actual content of the home screen popped
into view.

\*\*Goal:\*\* Remove the grey screen entirely and keep the full-page
skeleton loader active until the real data is fetched and ready to be
displayed.

\-\--

\## 2. Technical Investigation & Root Cause

The flicker was caused by two distinct issues occurring in sequence:

\### A. Premature Skeleton Removal

The previous implementation used
\`InteractionManager.runAfterInteractions\` to switch from the skeleton
to the real content. While this waits for the navigation transition to
finish, it does \*\*not\*\* wait for data fetching. The skeleton would
disappear, leaving the app to render sections that were still in a
\"Loading\" state.

\### B. The \"Grey Screen\" (Animation Delay)

The home screen sections (Trending, Events, etc.) use \`MotiView\` for
entry animations:

\`\`\`tsx

\<MotiView

from={{ opacity: 0, translateY: 20 }}

animate={{ opacity: 1, translateY: 0 }}

transition={{ duration: 400, delay: index \* 100 }}

\>

{content}

\</MotiView\>

\`\`\`

When the skeleton was removed, these components mounted and started at
\*\*0% opacity\*\*. For the first 400ms+, the user saw nothing but the
app\'s background color (grey), creating the \"grey screen\" effect.

\-\--

\## 3. The Solution: \"Background Preparation & Overlay Strategy\"

Instead of conditionally rendering either the Skeleton \*\*OR\*\* the
List, we now render \*\*both\*\* simultaneously in a stack.

\### Key File:
\[Home.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/founder/home/Home.tsx)

\#### Step 1: Integrated Data Tracking

We now monitor the specific query keys required for the home screen
using \`useIsFetching\` from React Query. This tells us exactly when the
background network calls are finished.

\`\`\`tsx

const trendingFetching = useIsFetching({ queryKey:
\[queryKeys.discussion.trendingFeed\] });

const eventsFetching = useIsFetching({ queryKey:
\[queryKeys.events.events\] });

const jobsFetching = useIsFetching({ queryKey:
\[queryKeys.jobs.getNormalJobPostings\] });

const mentorsFetching = useIsFetching({ queryKey:
\[queryKeys.misc.topMentors\] });

const communitiesFetching = useIsFetching({ queryKey:
\[queryKeys.community.recommendedCommunities\] });

const isDataFetching = trendingFetching \> 0 \|\| eventsFetching \> 0
\|\| jobsFetching \> 0 \|\| mentorsFetching \> 0 \|\|
communitiesFetching \> 0;

const showSkeleton = !isTransitionFinished \|\| isDataFetching;

\`\`\`

\#### Step 2: The Overlay Render

The \`FlatList\` is rendered immediately so that children can start
fetching data and running their animations. The
\`HomeScreenSkeletonLoader\` is placed in an \*\*absolute-positioned
overlay\*\* on top of the list.

\`\`\`tsx

return (

\<View style={{ flex: 1, backgroundColor: theme.colors.background }}\>

{/\* 1. Real content renders immediately underneath \*/}

\<Animated.FlatList

data={HomeData}

renderItem={renderItem}

\...

/\>

{/\* 2. Skeleton covers the list until ready \*/}

{showSkeleton && (

\<View style={{ position: \'absolute\', top: 0, left: 0, right: 0,
bottom: 0, backgroundColor: theme.colors.background, zIndex: 10 }}\>

\<View style={{ flex: 1, paddingTop: totalHeaderHeight }}\>

\<HomeScreenSkeletonLoader /\>

\</View\>

\</View\>

)}

{/\* 3. Header stays on top at all times \*/}

\<HomeHeader

navigation={navigation}

animatedStyle={animatedHeaderStyle}

isAbsolute={true}

/\>

\</View\>

);

\`\`\`

\-\--

\## 4. Best Practices Implemented

1\. \*\*Parallelization:\*\* By mounting the list behind an overlay,
data fetching starts the millisecond the screen is initialized, rather
than waiting for the skeleton to unmount.

2\. \*\*Hidden Animation Execution:\*\* Entry animations (\`MotiView\`)
play out while the skeleton is still visible. By the time the skeleton
unmounts, the content is already at 100% opacity, eliminating the grey
flicker.

3\. \*\*State Coordination:\*\* The UI only transitions when
\*\*both\*\* the JS thread is idle (\`InteractionManager\`) and the
Network cache is populated (\`useIsFetching\`).

4\. \*\*Z-Index Layering:\*\* Using absolute positioning for loaders
ensures that shared UI elements (like the \`HomeHeader\`) don\'t need to
re-mount or flicker during the transition.

\## 5. Reference Files

\- \*\*Logic:\*\*
\[Home.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/founder/home/Home.tsx)

\- \*\*Wrapper:\*\*
\[index.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/founder/home/index.tsx)

\- \*\*Skeleton:\*\*
\[HomeScreenSkeletonLoader.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/common/HomeScreenSkeletonLoader.tsx)

\- \*\*Query Keys:\*\*
\[queryKeys.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/api/queryKeys.ts)

# Problem 95

\# Bug Resolution Report: Home Header & Navigation Crash

This report details the investigation and resolution of two critical
bugs: the unresponsiveness of the Home screen header icons after
scrolling and the \`Maximum update depth exceeded\` crash occurring
during navigation.

\## 1. Problem Description

\### Issue A: \"Nothing happens\" on Icon Click

After scrolling the Home screen down and back up, the top header icons
(Avatar, AI Chat Bot, Notifications) became unresponsive to touch on
Android. Although visible, clicking them did not trigger navigation.

\### Issue B: \"Maximum update depth exceeded\" Crash

When attempting to navigate to screens that utilized the \`TopHeader\`
component (such as Profile or Chat Bot), the application would
frequently crash with a React \"Render Error\" stating that the maximum
update depth was exceeded.

\-\--

\## 2. Technical Investigation & Solution

\### Cause Analysis

1\. \*\*Gesture Boundary Desync (Android):\*\* The \`HomeHeader\` uses
an absolute position and a Reanimated \`translateY\` transform to
hide/show during scroll. On Android, \`MotiPressable\` (which uses
\`react-native-gesture-handler\`) often fails to synchronize its
hit-test bounds with native-thread transforms. This left the
\"clickable\" area stuck off-screen even when the visual icon was back
at the top.

2\. \*\*Infinite State Loop (Zustand):\*\* The \`useTheme\` hook was
triggering an \`updateTheme\` call inside a \`useEffect\`. Because the
\`themeStore\` lacked a referential equality check, every \`set\` call
created a new state object, which triggered all listeners (components
using the theme), which then re-ran their effects, causing an infinite
loop.

\### Implementation Details

\#### \[MODIFY\]
\[HomeHeader.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/home/HomeHeader.tsx)

Replaced \`MotiPressable\` with \`TouchableOpacity\` to use the React
Native JS responder system, which correctly handles native transforms on
Android.

\`\`\`tsx

// Before

\<MotiPressable onPress={() =\> navigateFromTab(navigation,
SCREEN_NAMES.CHAT_BOT)}\>

\<MotiView \...\>

\<Icon source=\"robot\" /\>

\</MotiView\>

\</MotiPressable\>

// After

\<TouchableOpacity onPress={() =\> navigateFromTab(navigation,
SCREEN_NAMES.CHAT_BOT)} activeOpacity={0.7}\>

\<MotiView \...\>

\<Icon source=\"robot\" /\>

\</MotiView\>

\</TouchableOpacity\>

\`\`\`

\#### \[MODIFY\]
\[themeStore.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/store/themeStore.ts)

Added a defensive equality check to prevent redundant state updates that
trigger listener loops.

\`\`\`tsx

updateTheme: (systemColorScheme?: \'light\' \| \'dark\' \| null) =\> {

const newTheme = get().getTheme(systemColorScheme);

// Defensive check: only set state if the theme object reference has
changed

if (get().currentTheme !== newTheme) {

set({ currentTheme: newTheme });

}

},

\`\`\`

\#### \[MODIFY\]
\[useTheme.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/hooks/useTheme.ts)

Removed the stable \`updateTheme\` action from the \`useEffect\`
dependency array to eliminate potential cyclic triggers.

\`\`\`tsx

useEffect(() =\> {

if (themeMode === \'system\') {

updateTheme(systemColorScheme ?? \'light\');

}

// Removed updateTheme from dependencies

}, \[systemColorScheme, themeMode\]);

\`\`\`

\-\--

\## 3. Files Modified

\-
\[src/components/home/HomeHeader.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/home/HomeHeader.tsx)

\-
\[src/store/themeStore.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/store/themeStore.ts)

\-
\[src/hooks/useTheme.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/hooks/useTheme.ts)

\-\--

\## 4. Best Practices for Future Reference

1\. \*\*Touchables vs Gesture Handlers:\*\* When a component is being
translated using native Reanimated transforms (like a sticky or hiding
header), prefer standard React Native \`TouchableOpacity\` or
\`Pressable\` over \`react-native-gesture-handler\` based components
(\`MotiPressable\`) on Android. The JS responder system is more reliable
for tracking hit-bounds on transformed views.

2\. \*\*Zustand State Guarding:\*\* Always implement a reference check
(\`if (state.prop !== newValue)\`) before calling \`set()\` inside
Zustand actions if those actions are likely to be called from
\`useEffect\` hooks. This prevents infinite render-loop crashes.

3\. \*\*Stable Dependency Management:\*\* Actions returned from a
Zustand store are stable. To avoid unnecessary \`useEffect\` triggers,
consider omitting them from dependency arrays if they are used to update
the same state that the hook is subscribing to.

4\. \*\*Interaction Management:\*\* Use
\`InteractionManager.runAfterInteractions\` for heavy logic or state
updates during screen transitions, but ensure no infinite animations
(like \`loop: true\` in Moti) are running, as they will block the
completion of interactions.

# Problem 96

\# Analysis Report: Delayed Search History Updates

\## 1. The Problem

Users observed that new search terms (e.g., \"Super Mario\") would not
appear in the \*\*Recent Searches\*\* list immediately after being
typed. The list only updated after a full application restart or device
reconnection.

\*\*Technical Root Cause:\*\*

The \`useGetRecentSearches\` hook was fetching data correctly on the
initial component mount. However, when a search was performed, the
backend would update the user\'s history, but the frontend was still
holding onto the \"stale\" (old) cached data from the first load.
Because there was no trigger to tell React Query to fetch the list
again, the UI remained unchanged until the component was forced to
remount (by restarting the app).

\## 2. The Solution

We implemented a reactive trigger that forces a refresh of the history
data as soon as it is needed---specifically, when the user clears their
search query to view the history list.

\### Affected File

\`src/screens/search/Search.tsx\`

\### The Fix (Code Snippet)

\`\`\`typescript

// Inside the Search component

const {

data: recentSearchesData,

refetch: refetchHistory,

} = useGetRecentSearches(4);

React.useEffect(() =\> {

// CRITICAL FIX: Instantly refresh recent searches when the user clears
the input.

// This ensures that any search performed just seconds ago is fetched
from

// the server before the Recent Searches list is displayed.

if (!debouncedSearchQuery \|\| debouncedSearchQuery.trim().length === 0)
{

refetchHistory();

}

}, \[debouncedSearchQuery, refetchHistory\]);

\`\`\`

\## 3. Why this works

1\. \*\*State Synchronization:\*\* By linking the \`refetchHistory\`
function to the \`debouncedSearchQuery\` state, we ensure the frontend
stays in sync with the backend.

2\. \*\*User Experience (UX):\*\* The user typically clears the search
bar when they are done searching or want to see their previous searches.
By refetching at this exact moment, we provide the most relevant,
up-to-date data exactly when the user is looking for it.

\## 4. Best Practices for Future Reference

\* \*\*Invalidate on Mutation:\*\* Whenever you perform an action that
changes data on the server (like searching, which adds a history
record), ensure the corresponding \"GET\" queries are invalidated or
refetched.

\* \*\*Reactive Refetching:\*\* Use \`useEffect\` to trigger refetches
when a user\'s intent changes (e.g., switching tabs or clearing
filters).

\* \*\*Stale Time Management:\*\* In React Query, if data is highly
dynamic, set \`staleTime: 0\` to ensure it\'s always considered old and
ready for a refresh, but remember you still need a \"trigger\" (like a
mount or an explicit refetch) to start the network request.

\* \*\*Avoid \"Ghost\" Data:\*\* Never assume that just because a user
performed an action, the UI will update automatically. Always explicitly
manage the lifecycle of your cached data.

# Problem 97

\# Search Trigger Behavior Report

This report documents the optimization of the search functionality
within the mobile application, shifting from an automatic debounced
trigger to an explicit user-initiated trigger.

\## 1. The Problem

Previously, the search functionality was implemented using a
\*\*debounce\*\* pattern. This meant that every time a user typed a
character, a 500ms timer would start. If the user typed slowly or
paused, the search would automatically trigger in the middle of their
typing.

\### Issues with the Previous Approach:

\- \*\*Poor UX:\*\* Results would jump and change while the user was
still composing their query.

\- \*\*Unnecessary API Load:\*\* Multiple partial searches were sent to
the backend as the user typed.

\- \*\*Visual Distraction:\*\* The loading skeletons and result
transitions were triggered prematurely, creating a \"flickering\" effect
for slow typers.

\## 2. Solution Implementation

The search logic was decoupled from the input state. We introduced a
distinction between the \*\*typing state\*\* (\`searchQuery\`) and the
\*\*applied state\*\* (\`appliedSearchQuery\`).

\### File:
\[HomeHeader.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/home/HomeHeader.tsx)

We enabled the UI to capture search intents via the keyboard and the
search icon.

\`\`\`tsx

// Added onSearchSubmit prop and keyboard integration

\<TextInput

value={searchQuery}

onChangeText={onSearchChange}

onSubmitEditing={onSearchSubmit} // Trigger on Enter key

returnKeyType=\"search\" // Changes \"Enter\" to \"Search\" on keyboard

// \...

/\>

// Made the magnifying glass icon clickable

\<TouchableOpacity onPress={onSearchSubmit} activeOpacity={0.7}\>

\<Icon source=\"magnify\" size={20} /\>

\</TouchableOpacity\>

\`\`\`

\### File:
\[Search.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/search/Search.tsx)

We replaced the \`useEffect\` debounce logic with explicit handler
functions.

\`\`\`tsx

// Explicit state for applied search

const \[appliedSearchQuery, setAppliedSearchQuery\] =
React.useState(\'\');

// Function to \"commit\" the search

const handleSearch = React.useCallback(() =\> {

if (searchQuery.trim().length \> 0) {

setAppliedSearchQuery(searchQuery);

}

}, \[searchQuery\]);

// Function to handle typing and instant clear

const handleSearchChange = React.useCallback((text: string) =\> {

setSearchQuery(text);

// Clear results immediately if the input is emptied

if (!text \|\| text.trim().length === 0) {

setAppliedSearchQuery(\'\');

}

}, \[\]);

\`\`\`

\## 3. Impact of Changes

\- \*\*Predictability:\*\* Results only appear when the user is \"done\"
and clicks Search.

\- \*\*Cleaner UX:\*\* Typing is now a fluid experience without
premature loading states.

\- \*\*Efficiency:\*\* Drastic reduction in the number of search API
calls.

\## 4. Best Practices for Future Reference

When implementing search in React Native, follow these guidelines for
the best user experience:

1\. \*\*Explicit vs. Implicit Trigger:\*\*

\* \*\*Use Implicit (Debounce)\*\* when the search space is small (like
filtering a local list) or when you have a very fast/efficient
autocomplete API.

\* \*\*Use Explicit (Submit)\*\* for complex, paginated, or expensive
global searches (like People, Companies, Jobs).

2\. \*\*Keyboard Configuration:\*\* Always set
\`returnKeyType=\"search\"\` and implement \`onSubmitEditing\`. Mobile
users expect the blue \"Search\" button on their keyboard to work.

3\. \*\*Instant Clear:\*\* Even if the search trigger is explicit, the
\*\*clear\*\* action (clicking the \'x\' or deleting all text) should
always be \*\*instant\*\*. This allows the user to quickly return to
their \"Recent Searches\" or default state without extra clicks.

4\. \*\*Visual Feedback:\*\* Ensure that when the search is triggered,
the user receives immediate feedback (e.g., a loading indicator or
skeleton screen) to acknowledge their action.

# Problem 98

\# Search Screen Chip Content Bug Fix Report

This report summarizes the fix for the issue where active search chips
failed to display content when the search input was empty.

\## 1. The Problem

On the Search screen, selecting a category chip (e.g., \"People\",
\"Companies\") without entering text in the search bar resulted in only
\"Recent Searches\" being displayed. The expected behavior was to see
the \"Recent Searches\" list followed by the content relevant to the
active chip (e.g., trending people or suggested companies).

The root cause was two-fold:

\- \*\*Query Disabling:\*\* The API fetching hooks were conditionally
disabled when the search query was empty.

\- \*\*Rendering Short-circuit:\*\* The UI rendering logic returned
early if no search query was present, blocking any chip-specific
sections from being rendered.

\## 2. File Names

\- \`src/screens/search/Search.tsx\`

\## 3. Important Code Snippets

\### Enabling API Fetching for Empty Queries

The \`enabled\` condition was modified to allow the API to fetch
default/trending data even when \`appliedSearchQuery\` is empty.

\`\`\`tsx

// Before

const standardQuery = useGetSearchedData(searchPayload, { enabled:
!isScoped && hasQueryText });

const infiniteQuery = useGetSearchedDataInfinite(searchPayload, {

enabled: isScoped && hasQueryText,

// \...

});

// After

const standardQuery = useGetSearchedData(searchPayload);

const infiniteQuery = useGetSearchedDataInfinite(searchPayload, {

enabled: isScoped,

// \...

});

\`\`\`

\### Stacking Recent Searches and Chip Content

The \`renderTabContent\` function was refactored to compose the UI
instead of using early returns.

\`\`\`tsx

// Modified Logic

const renderTabContent = React.useCallback(() =\> {

let recentSearchesSection = null;

// 1. Prepare Recent Searches if no query text

if (!hasQueryText) {

recentSearchesSection = (

\<RecentSearchesList \... /\>

);

}

// 2. Prepare Results

if (!searchData) {

if (!hasQueryText) return recentSearchesSection;

return \<NoDataFound \... /\>;

}

// 3. Render Both Stacked

return (

\<View\>

{recentSearchesSection}

{showPeople && \<PeopleSection \... /\>}

{showCompanies && \<CompaniesSection \... /\>}

{/\* \... other sections \... \*/}

\</View\>

);

}, \[\...\]);

\`\`\`

\## 4. Best Practices for Future Reference

\- \*\*Avoid Early Returns for Layered UI:\*\* In screens where multiple
sections (like history and results) can coexist, avoid using \`if
(condition) return \...\` mid-way through the render function. Instead,
build segments into variables and render them together in a single
return block.

\- \*\*Support \"Empty Query\" States:\*\* Design API integrations to
handle empty search queries gracefully. Many backends return
\"Trending\" or \"Featured\" items when no search term is provided,
providing a better user experience than a blank screen.

\- \*\*Decouple Tab Logic from Search Logic:\*\* Ensure that selecting a
tab/chip always triggers a data refresh for that specific scope,
regardless of whether the user has started typing.

\- \*\*Use Fragment/View Composition:\*\* When stacking multiple
conditional lists, wrap them in a container to maintain layout
consistency and simplify the logic.

# Problem 99

## **Technical Report: Android TextInput Cursor Sync Issue**

This report outlines the technical challenge encountered with the
**Android Cursor Jump/Lock** bug in React Native, the implementation of
a resilient fix, and best practices for future development.

### **1. The Problem: Android Native Cursor Hijacking**

On Android, TextInput components frequently suffer from a bug where the
cursor forcefully jumps to the end of the text string or becomes
\"locked,\" preventing users from selecting or editing text in the
middle of a word.

**Technical Root Causes:**

- **Native Reset:** The bug originates in the Android native layer
  (ReactEditText.kt), where programmatic text updates---intended to
  clear composing text from buggy keyboards---accidentally reset the
  EditText state, placing the cursor at the default (end) position.

- **State Conflict:** In controlled components, if the value prop is
  tied directly to a state that updates on every keystroke (such as with
  **React Hook Form** in onChange mode), React Native reapplies the
  value to the native view. This constant \"push\" from JavaScript to
  Native overrides the native cursor\'s internal position.

- **Layout Interference:** Common workarounds like multiline={true} can
  fix the cursor but may conflict with KeyboardAvoidingView or specific
  CSS heights (as seen in the **Signup Screen**), leading to layout
  collapses or broken touch targets.

### **2. Affected Files**

- **TextInputField.tsx**: The primary shared component where the logic
  was abstracted to protect all inputs globally.

- **RegistrationScreen.tsx**: Specifically impacted due to complex form
  validation and the presence of KeyboardAvoidingView.

- **LoginScreen.tsx**: Impacted by the standard Android controlled-input
  behavior.

### **3. Implementation: The \"Safe Sync\" Pattern**

To resolve this without breaking layout or masking (for passwords), a
**local state buffer** is used. This decouples the immediate UI feedback
from the heavier parent re-render cycle.

#### **Core Logic: SafeControlledInput**

This internal wrapper ensures that the native cursor is only moved by
the user\'s typing, not by the state being pushed back down from the
parent.

TypeScript

const SafeControlledInput = ({ field, config, \...props }) =\> {

const { onChange, onBlur, value, ref } = field;

// 1. Maintain a local copy of the value for the UI

const \[internalValue, setInternalValue\] = useState(value ?? \'\');

const isTyping = useRef(false);

useEffect(() =\> {

// 2. Only sync from the parent if the change was NOT triggered by
typing

// (e.g., an Autofill button or external reset).

if (!isTyping.current && value !== internalValue) {

setInternalValue(value ?? \'\');

}

isTyping.current = false;

}, \[value\]);

return (

\<TextInput

{\...config}

ref={ref}

value={internalValue} // 3. Use the buffered local state

onChangeText={(text) =\> {

isTyping.current = true; // 4. Flag that the user is currently typing

setInternalValue(text); // 5. Update UI instantly

onChange(text); // 6. Update Form State in the background

}}

onBlur={onBlur}

// \...rest of props

/\>

);

};

### **4. Best Practices for Future Reference**

To maintain high-quality input performance in React Native, follow these
principles:

  --------------------------------------------------------------------------
  **Principle**         **Description**
  --------------------- ----------------------------------------------------
  **Buffer Controlled   For complex forms on Android, always use a local
  Inputs**              state buffer to prevent \"fighting\" between the
                        Native cursor and JS state.

  **Avoid multiline     While multiline={true} is a common suggestion, it
  Hacks**               breaks secureTextEntry and can cause layout issues
                        in ScrollView containers.

  **Platform-Specific   Always test input behavior on both a **Physical
  Testing**             Android Device** and an **Emulator**, as native
                        keyboard behaviors (like Gboard auto-suggestions)
                        vary significantly between them.

  **Stabilize Props**   Use useMemo for style objects and outlineStyle to
                        prevent React Native Paper from losing internal
                        state during rapid re-renders.

  **Backward            When updating shared components, wrap new logic in
  Compatibility**       internal sub-components or optional props to ensure
                        existing screens do not break (The Golden Rule).
  --------------------------------------------------------------------------

By adopting the **Safe Sync** pattern, the application achieves smooth,
native-feeling text interaction while retaining the full power of
centralized validation and state management.

# Problem 100

\# Walkthrough - Event Refresh Fix

I have resolved the issue where newly created events were not appearing
in the \"My Upcoming Events\" and \"Other Events\" sections of the
parent Events screen.

\## Changes

\### API Hooks standardization

I updated \`src/api/hooks/useEvents.ts\` to standardize how query keys
are constructed.

Previously, some hooks used nested arrays for query keys (e.g.,
\`\[queryKeys.events.eventList, params\]\`), which prevented the parent
key \`\[\'apps\', \'events\'\]\` from correctly invalidating them during
event creation.

By using the spread operator (\`\[\...queryKeys.events.eventList,
params\]\`), all event-related queries are now correctly caught by the
standard invalidation logic.

\### Automatic Focus Refresh

I re-enabled \`useFocusEffect\` in \`src/screens/events/Events.tsx\`.
This ensures that whenever a user navigates back to the Events screen
(e.g., after creating an event), the application automatically triggers
a refetch of all event data, including categories and upcoming events.

\## Verification Results

\### Logic Verification

\- \*\*Standardized Keys\*\*: Verified that all query keys in
\`useEvents.ts\` now follow a flat structure that supports prefix-based
invalidation.

\- \*\*Invalidation Match\*\*: Confirmed that
\`queryKeys.events.events\` (\`\[\'apps\', \'events\'\]\`) now correctly
matches \`queryKeys.events.eventList\` (\`\[\'apps\', \'events\',
\'eventList\', \...\]\`).

\- \*\*Focus Refetch\*\*: Verified that \`Events.tsx\` now calls
\`refetchUpcoming()\`, \`refetchOther()\`, and \`refetchCategories()\`
when focused.

\### UI behavior

\- After creating an event, the user is navigated back to the Events
screen.

\- The \`useFocusEffect\` triggers a background refetch.

\- The new event appears in the relevant sections based on its ownership
and category.

# Problem 101

\# Technical Report: Resolving Job Refresh Issues

\## 1. Problem Description

Users reported that newly created jobs were not appearing in two
critical areas of the application:

1\. \*\*Company Profile (Jobs Tab)\*\*: After creating a job, the list
remained outdated until a manual refresh.

2\. \*\*Home Screen (Job Opportunities)\*\*: The dashboard section did
not reflect the latest job postings.

\### Root Causes

\- \*\*Inconsistent Query Keys\*\*: Some hooks used nested arrays (e.g.,
\`\[\[key\], params\]\`), while invalidations used flat arrays
(\`\[key\]\`). React Query\'s prefix matching does not work across
nested boundaries.

\- \*\*Missing Mutation Callbacks\*\*: The \`useCreateJobPosting\` and
\`useUpdateJobPosting\` hooks lacked \`onSuccess\` handlers to
invalidate the cache.

\- \*\*Missing Focus-Based Refetching\*\*: Screens were showing cached
(stale) data because they didn\'t trigger a refetch when the user
navigated back to them.

\-\--

\## 2. Implementation Details

\### File: \`src/api/hooks/useJobPosting.ts\`

We standardized the query keys and added the necessary invalidation
logic.

\*\*Standardized Query Key Pattern:\*\*

\`\`\`typescript

// BEFORE: Nested (Incorrect for prefix matching)

queryKey: \[queryKeys.jobs.getNormalJobPostings, params\]

// AFTER: Flattened (Correct)

queryKey: \[\...queryKeys.jobs.getNormalJobPostings, params\]

\`\`\`

\*\*Added Invalidation Logic:\*\*

\`\`\`typescript

export const useCreateJobPosting = () =\> {

return useMutation({

mutationKey: queryKeys.jobs.createJob,

mutationFn: (payload: any) =\> createJob(payload),

onSuccess: () =\> {

// Invalidate everything under the jobs root to ensure total sync

queryClient.invalidateQueries({

queryKey: \[\'apps\', \'jobs\'\],

});

},

});

};

\`\`\`

\### File: \`src/screens/companyprofile/JobTab.tsx\` &
\`src/components/home/JobOpportunities.tsx\`

We re-enabled \`useFocusEffect\` to ensure that data is refetched
whenever the user views these sections.

\`\`\`typescript

useFocusEffect(

React.useCallback(() =\> {

refreshJobPosting(); // Triggers a background refetch

}, \[refreshJobPosting\])

);

\`\`\`

\-\--

\## 3. Best Practices for Future Reference

To avoid similar issues in the future, follow these guidelines when
working with React Query and navigation:

\### A. Flat Query Keys

Always use the spread operator when extending a base query key. This
ensures that invalidating a parent key (e.g., \`\[\'apps\',
\'jobs\'\]\`) correctly clears all related child queries (e.g.,
\`\[\'apps\', \'jobs\', \'list\', { id: 1 }\]\`).

\> \[!TIP\]

\> \*\*Correct:\*\* \`queryKey: \[\...baseKey, params\]\`

\> \*\*Incorrect:\*\* \`queryKey: \[baseKey, params\]\`

\### B. Mandatory Mutation Invalidations

Every \"Write\" operation (Create, Update, Delete) \*\*must\*\* have an
\`onSuccess\` block that invalidates the relevant \"Read\" queries.

\- Use the most specific key possible if only one item changed.

\- Use a broader parent key if the change affects lists or counts.

\### C. Navigation-Aware Refetching

In React Native, screens often stay mounted in the background. Use
\`useFocusEffect\` from \`@react-navigation/native\` to trigger
refetches when a user returns to a screen. This is especially important
for parent screens that a user returns to after completing a task in a
child screen.

\### D. Consistent Key Definitions

Maintain all query keys in \`src/api/queryKeys.ts\` and always use them
via the constant object rather than hardcoding strings. This ensures
that a single change in the key structure propagates correctly
throughout the app.

\-\--

\## 4. Conclusion

By standardizing the query key structure and ensuring both proactive
(mutation-based) and reactive (focus-based) refreshes, the Jobs module
is now consistent and real-time across all application views.

# Problem 102

\# Navigation Fix Report: Post Creation Flow

\## 1. The Problem

\### Issue A: Stack Pollution (Back Button Loop)

When a user successfully created a new post, the application navigated
to the \`CommunityDetail\` screen using \`navigation.navigate\`. In
React Navigation, this pushes the new screen onto the stack.
Consequently, when the user pressed the back button on the
\`CommunityDetail\` page, they were returned to the \`CreatePost\`
screen (New Post form) instead of the main Feed.

\### Issue B: Nested Navigation Action Error

When attempting to fix the above by explicitly navigating to the
\`CommunityDashboard\` from \`CommunityDetail\`, the application threw a
console error:

\> \*\"The action \'NAVIGATE\' with payload
{\"name\":\"CommunityDashboard\"} was not handled by any navigator.\"\*

This occurred because \`CommunityDashboard\` is a \*\*tab\*\* nested
inside the \`MainStack\` (or \`InvestorStack\`). A screen at the Root
level (like \`CommunityDetail\`) cannot navigate directly to a nested
sub-screen without referencing the parent stack.

\-\--

\## 2. Important Code Solutions

\### A. Cleaning the Navigation Stack

We changed the navigation method in the post creation success callback
from \`navigate\` to \`replace\`. This removes the \"New Post\" screen
from the history entirely.

\*\*File:\*\*
\[CreatePost.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/community/CreatePost.tsx)

\`\`\`tsx

// BEFORE

navigation.navigate(\'CommunityDetails\', { \... });

// AFTER

navigation.replace(SCREEN_NAMES.COMMUNITY_DETAILS, {

\...params,

fromPostCreation: true, // Flag to identify the source

});

\`\`\`

\### B. Explicit Nested Navigation

We implemented a custom back button handler that identifies the correct
parent stack based on the user\'s role and uses nested navigation
syntax.

\*\*File:\*\*
\[CommunityDetail.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/community/CommunityDetail.tsx)

\`\`\`tsx

onBackPress={() =\> {

if (fromPostCreation) {

const userType = useAuthStore.getState().userType;

const isInvestor = userType === \'investor\' \|\| userType ===
\'Investor\';

// Explicitly target the parent stack to reach the nested tab

const targetStack = isInvestor ? STACK_NAMES.INVESTOR :
STACK_NAMES.MAIN;

navigation.navigate(targetStack as any, {

screen: SCREEN_NAMES.COMMUNITY_DASHBOARD,

});

} else {

navigation.goBack();

}

}}

\`\`\`

\-\--

\## 3. Files Involved

\| File Name \| Role \|

\| :\-\-- \| :\-\-- \|

\| \`src/types/navigation.ts\` \| Updated parameter types to include
\`fromPostCreation\`. \|

\| \`src/screens/community/CreatePost.tsx\` \| Switched to \`replace()\`
and passed the state flag. \|

\| \`src/screens/community/CommunityDetail.tsx\` \| Implemented custom
back-button logic with nested stack routing. \|

\-\--

\## 4. Best Practices for Future Reference

\### 1. Use \`replace()\` for \"Final\" Actions

When moving a user from a \"Form\" or \"Process\" screen (like Post
Creation, Login, or Checkout) to a \"Result\" or \"Detail\" screen,
always use \`navigation.replace()\`. This prevents the user from
navigating back into a stale or completed state.

\### 2. Nested Navigation Requires Parent Scoping

If you are navigating from a sibling screen (Root level) to a screen
inside a Tab or Drawer navigator, you \*\*must\*\* use the nested
navigation object format:

\`\`\`tsx

navigation.navigate(\'ParentStackName\', {

screen: \'TargetSubScreenName\',

params: { \... }

});

\`\`\`

\### 3. Contextual Navigation Flags

Use optional boolean flags (like \`fromPostCreation\`) in route params
to slightly modify the behavior of shared screens based on where the
user came from. This is more flexible than creating duplicate screens.

\### 4. Role-Based Stack Resolution

In apps with multiple main stacks (e.g., Founder vs. Investor), always
resolve the target stack dynamically from your global state
(Zustand/Redux) before performing cross-stack navigation.

# Problem 103

Viewed CreateEvent.tsx:693-703

I have compiled a detailed report regarding the event time validation
issue and its resolution. You can find this report below and also saved
as a persistent artifact for your records.

\# Event Time Validation Report

\### 1. The Problem

In the event creation form, users were able to select an end time that
occurred before the start time when both the start and end dates were
the same. This resulted in logically impossible event durations (e.g.,
Start: 5:04 PM, End: 5:03 PM) which could cause issues with backend
processing or display logic.

\### 2. Affected Files

\- \*\*Primary Logic\*\*: \`src/screens/events/CreateEvent.tsx\`

\- \*\*Component Layer\*\*: \`src/components/forms/FormInput.tsx\`
(utilizing \`DatePickerField.tsx\`)

\### 3. Key Code Implementations

\#### A. Picker Constraint Logic

We restricted the date and time pickers so that users cannot select an
invalid range in the first place.

\`\`\`typescript

// For the End Date field

minimumDate: eventDate \|\| new Date()

// For the End Time field (Dynamic restriction)

minimumDate: isSameDay(eventDate, endDate) ? eventTime : undefined

\`\`\`

\#### B. Auto-Adjustment (UX Enhancement)

To make the form more intuitive, we added \`useEffect\` hooks that
automatically adjust the end values if the start values are moved past
them.

\`\`\`typescript

// Auto-adjust end time if it\'s before event time on the same day

useEffect(() =\> {

if (isSameDay(eventDate, endDate) && eventTime && endTime && endTime \<
eventTime) {

setValue(\'endTime\', eventTime);

}

}, \[eventDate, endDate, eventTime, endTime, setValue\]);

\`\`\`

\#### C. Schema-Level Validation (Zod)

As a final layer of protection, the validation schema enforces the rule,
ensuring the form cannot be submitted if the logic is bypassed.

\`\`\`typescript

.refine(

data =\> {

if (data.eventDate && data.endDate) {

if (isSameDay(data.eventDate, data.endDate) && data.eventTime &&
data.endTime) {

return data.endTime.getTime() \>= data.eventTime.getTime();

}

}

return true;

},

{

message: \'End time cannot be earlier than start time on the same day\',

path: \[\'endTime\'\],

}

)

\`\`\`

\### 4. Best Practices for Future Reference

1\. \*\*Prevent at the Source\*\*: Always use the \`minimumDate\` or
\`maximumDate\` properties on date pickers to disable invalid options.
This provides the best UX by preventing errors before they happen.

2\. \*\*Reactive Form Dependencies\*\*: When one form field depends on
another (like Start/End times), use \`watch\` and \`useEffect\` to keep
them synchronized. This reduces manual correction work for the user.

3\. \*\*Cross-Field Validation\*\*: Standard field validation (e.g.,
\`required\`) isn\'t enough for logical ranges. Use Zod\'s \`.refine()\`
or \`.superRefine()\` to validate the relationship between multiple
fields.

4\. \*\*Date Object Normalization\*\*: When comparing dates for
\"sameness,\" ensure you normalize or ignore the time component (using a
helper like \`isSameDay\`) to avoid unexpected results due to
milliseconds or time zones.

# Problem 104

\# Walkthrough - Fixed Search in AutocompleteField

I have implemented client-side filtering in the \`AutocompleteField\`
component. This ensures that when a user searches in a modal that uses
local options (like the Event Category modal), the list updates to show
only matching results.

\## Changes Made

\### Form Components

\####
\[AutocompleteField.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/forms/AutocompleteField.tsx)

\- Added logic to filter options locally when \`searchType\` is not a
server-side type.

\- The filtering is case-insensitive and matches substrings in the
option labels.

\- Added support for a custom \`filterFunction\` prop.

\- Updated the \`useMemo\` dependency array to include all relevant
state and props.

\## Verification Results

\### Automated Tests

\- No automated tests were run, but the logic was verified by reviewing
the code and ensuring it follows the existing patterns in the codebase.

\### Manual Verification

\- The search bar in the \"Event Category\" modal now correctly filters
the list of categories as the user types.

\- The search is immediate (non-debounced) for local options, providing
a snappy user experience.

\- Server-side searches (like Location) continue to use the debounced
API-based filtering as before.

# Problem 105

\# Technical Report: Event Filtering Resolution

\## 1. Problem Description

The application\'s event filtering system failed to update the UI when
users selected specific category chips (e.g., \"Anime & Cosplay\") in
the filter modal. Even after clicking \"Apply Filters,\" the list
continued to display all created events instead of a filtered subset.

\### Root Causes

\- \*\*Backend Discrepancy\*\*: The endpoint for fetching a user\'s own
events (\`events/me\`) did not strictly filter results by \`categoryId\`
on the server side.

\- \*\*Missing Frontend Logic\*\*: The \`EventList\` component relied
entirely on the API response for filtering. It lacked a local filtering
fallback for categories, locations, and timeframes.

\- \*\*Stale Memoization\*\*: The \`eventsList\` \`useMemo\` hook was
missing the \`filters\` state in its dependency array. This meant that
even if the filtering logic existed, it wouldn\'t have re-triggered when
the user changed filter selections without also changing the search
text.

\-\--

\## 2. Affected Files

\- \*\*Primary Logic\*\*: \`src/screens/events/EventList.tsx\`

\- \*\*UI State Source\*\*: \`src/screens/events/EventFiltersModal.tsx\`

\- \*\*Navigation/Parent\*\*: \`src/screens/events/Events.tsx\`

\-\--

\## 3. Implementation Details

\### Before Change (Incomplete Filtering)

The list only manually filtered for the search query and lacked the
\`filters\` dependency:

\`\`\`tsx

// src/screens/events/EventList.tsx (Old Version)

const eventsList = useMemo(() =\> {

if (!eventsData?.pages) return \[\];

const allEvents = eventsData.pages.flatMap((page: any) =\> pathOr(\[\],
\[\'data\', \'events\'\], page));

// \... de-duplication logic \...

let finalEvents = Array.from(uniqueEvents.values());

// ONLY filtered by search query

if (debouncedSearchQuery.trim()) {

const query = debouncedSearchQuery.toLowerCase();

finalEvents = finalEvents.filter(event =\>
event.title?.toLowerCase().includes(query));

}

return finalEvents;

}, \[eventsData, debouncedSearchQuery\]); // Missing \'filters\'
dependency

\`\`\`

\### After Change (Robust Filtering)

I implemented a comprehensive frontend filtering layer and added the
necessary dependencies:

\`\`\`tsx

// src/screens/events/EventList.tsx (New Version)

const eventsList = useMemo(() =\> {

if (!eventsData?.pages) return \[\];

const allEvents = eventsData.pages.flatMap((page: any) =\> pathOr(\[\],
\[\'data\', \'events\'\], page));

// \... de-duplication logic \...

let finalEvents = Array.from(uniqueEvents.values());

// 1. Filter by Search Query

if (debouncedSearchQuery.trim()) {

const query = debouncedSearchQuery.toLowerCase();

finalEvents = finalEvents.filter(event =\>
event.title?.toLowerCase().includes(query));

}

// 2. Filter by Category (FIXED)

if (filters.categoryId) {

finalEvents = finalEvents.filter(

event =\> String(event.category?.id) === String(filters.categoryId)

);

}

// 3. Filter by Location

if (filters.locationId) {

finalEvents = finalEvents.filter(

event =\> String(event.location?.id) === String(filters.locationId)

);

}

// 4. Filter by Timeframe (Parsed from \"X Days\" string)

if (filters.timeframe) {

const daysMatch = filters.timeframe.match(/\\d+/);

if (daysMatch) {

const days = parseInt(daysMatch\[0\], 10);

const limitDate = new Date();

limitDate.setDate(limitDate.getDate() + days);

limitDate.setHours(23, 59, 59, 999);

finalEvents = finalEvents.filter(event =\> {

if (!event.startAt) return false;

const eventDate = new Date(event.startAt);

return eventDate \<= limitDate;

});

}

}

return finalEvents;

}, \[eventsData, debouncedSearchQuery, filters\]); // Added \'filters\'
dependency

\`\`\`

\-\--

\## 4. Key Takeaways for Future Reference

1\. \*\*Frontend Fallback\*\*: When dealing with API-driven lists,
always implement a frontend filtering layer as a fallback. This ensures
the UI remains responsive and correct even if the backend behaves
inconsistently or during slow network updates.

2\. \*\*Memoization Dependencies\*\*: Always ensure that any state
variables used \*inside\* a \`useMemo\` or \`useCallback\` are included
in the dependency array. Failing to include \`filters\` was a primary
reason the UI didn\'t refresh upon clicking \"Apply Filters\".

3\. \*\*Type Safety\*\*: Use \`String()\` casting when comparing IDs
(e.g., \`event.category.id === filters.categoryId\`) to avoid mismatches
between string and numeric representations of IDs.

\-\--

\*\*Status\*\*: Resolved

\*\*Date\*\*: April 20, 2026

# Problem 106

\# Investigation Report: Community Detail Navigation Error (API 404)

\## 1. The Problem

When a user (specifically a community admin or owner) navigates to a
community detail page (e.g., \"John vick\"), the application
automatically attempts to fetch \*\*Pending Join Requests\*\*. This
operation fails with a \`404 Not Found\` error, which triggers a global
error toast and a console error.

\- \*\*Error Message\*\*: \`Not found -
/api/v1/community-membership/374/pending-requests\` (initially)

\- \*\*Impact\*\*: Disrupts the user experience on the Community Detail
screen with persistent error messages.

\-\--

\## 2. Root Cause Analysis

The issue is caused by an \*\*incorrect API endpoint path\*\* defined in
the centralized endpoints configuration. The application was trying to
access a resource path that does not exist on the server.

\### Path Inconsistency

In the \`COMMUNITIES\` API configuration:

\- \*\*Join Action\*\*: \`community-membership/\${communityId}/join\`
(Working)

\- \*\*List Requests\*\*:
\`/community-membership/\${communityId}/pending-requests\` (Incorrect -
404)

Additionally, there was an inconsistency with \*\*leading slashes\*\*.
Endpoints starting with \`/\` can sometimes bypass the \`baseURL\`
prefix (like \`/api/v1\`) depending on the Axios configuration, leading
to further 404s if the API is prefix-dependent.

\-\--

\## 3. Important Files & Code Snippets

\### File: \`src/api/endpoints.ts\`

This is the central location for all API URLs. The fix involves
correcting the path mapping.

\*\*Incorrect Code:\*\*

\`\`\`typescript

GET_PENDING_REQUESTS: (communityId: string \| number) =\>

\`/community-membership/\${communityId}/pending-requests\`,

\`\`\`

\*\*Corrected Code (Attempted Fix):\*\*

\`\`\`typescript

GET_PENDING_REQUESTS: (communityId: string \| number) =\>

\`community-membership/\${communityId}/requests\`,

\`\`\`

\*(Note: We are currently verifying if the plural \`/requests\` or a
query parameter \`?community_id=\` is the exact path required by the
backend).\*

\### File:
\`src/screens/community/components/community-detail/PendingRequests.tsx\`

This component triggers the API call whenever it is mounted (which
happens on the Community Detail screen for admins).

\`\`\`typescript

// Triggers the problematic API call

const { data: fetchedRequestsData, isFetching, refetch } =
useGetPendingRequests(communityId);

\`\`\`

\-\--

\## 4. Remediation Steps Taken

1\. \*\*Endpoint Correction\*\*: Updated \`src/api/endpoints.ts\` to
remove the leading slash and adjust the resource path to be more
consistent with the \`join\` action.

2\. \*\*Standardization\*\*: Removed leading slashes from related
endpoints (\`UPDATE_REQUEST_STATUS\`) to ensure they are always relative
to the \`/api/v1\` base URL.

3\. \*\*Cache Reset\*\*: Recommended a \`yarn start \--reset-cache\` to
ensure the new endpoint definitions are picked up by the app bundle.

\## 5. Future Reference

When adding new sub-resources to the \`COMMUNITIES\` or
\`COMMUNITY-MEMBERSHIP\` modules:

\- \*\*Always check the prefix\*\*: Use \`communities/\` for data
retrieval and \`community-membership/\` for relationship actions.

\- \*\*Check Pluralization\*\*: Backend resources are typically plural
(e.g., \`/requests\` instead of \`/request\`).

\- \*\*Avoid Leading Slashes\*\*: Keep paths relative to the base URL
defined in \`api/config.ts\`.

# Problem 107

\# Report: Event Location Filtering Fix

\## Problem Description

The event location filter was previously non-functional when users
searched for a location (e.g., \"Berlin\") but did not explicitly select
one of the autocomplete suggestions.

\*\*Technical Cause:\*\*

\- The system relied exclusively on \`locationId\` (a numeric/string ID
from the database) to perform filtering.

\- When a user types in the search box, the \`locationId\` is cleared
because the specific entity is no longer \"selected.\"

\- If the user clicked \"Apply Filters\" with only text in the search
box, the \`locationId\` was \`null\`, causing the filtering logic to
skip the location check entirely.

\- Additionally, reopening the filter modal would clear the search text
because it wasn\'t being synchronized from the parent\'s state.

\## Implementation Details

\### 1. Fallback Text-Based Filtering

We introduced a fallback mechanism in the manual filtering logic. If
\`locationId\` is missing, the system now matches the \`locationName\`
string against multiple fields in the event\'s location object.

\*\*Important Code Snippet (\`EventList.tsx\`):\*\*

\`\`\`typescript

// Manual filtering logic enhancement

if (filters.locationId) {

finalEvents = finalEvents.filter(

event =\> String(event.location?.id) === String(filters.locationId)

);

} else if (filters.locationName) {

const query = filters.locationName.toLowerCase();

finalEvents = finalEvents.filter(event =\> {

const city = event.location?.city?.toLowerCase() \|\| \'\';

const state = event.location?.state?.toLowerCase() \|\| \'\';

const country = event.location?.country?.toLowerCase() \|\| \'\';

const address = event.location?.addressLine?.toLowerCase() \|\| \'\';

return (

city.includes(query) \|\|

state.includes(query) \|\|

country.includes(query) \|\|

address.includes(query)

);

});

}

\`\`\`

\### 2. State Synchronization & Persistence

The \`EventFiltersModal\` was updated to accept \`selectedLocationName\`
as a prop. This ensures that even if a user hasn\'t selected a
suggestion, their search string is preserved and displayed when they
reopen the modal.

\*\*Important Code Snippet (\`EventFiltersModal.tsx\`):\*\*

\`\`\`typescript

useEffect(() =\> {

if (visible) {

setLocalFilter(selectedFilter);

setLocalTimeframe(selectedTimeframe);

setLocalLocationId(selectedLocationId);

// Initialize text from selectedLocationName if present

if (selectedLocationName) {

setLocalLocationText(selectedLocationName);

} else if (!selectedLocationId) {

setLocalLocationText(\'\');

}

setShowSuggestions(false);

}

}, \[visible, selectedFilter, selectedTimeframe, selectedLocationId,
selectedLocationName\]);

\`\`\`

\### 3. API Parameter Expansion

We included \`locationName\` in the \`queryParams\` passed to the
\`useEventsInfiniteQuery\` hook. This allows the backend to potentially
handle the string-based search if implemented in the future.

\## Files Modified

For future reference, the following files contain the core filtering
logic for events:

1\.
\*\*\[EventList.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/events/EventList.tsx)\*\*:

\* Contains the \`queryParams\` construction.

\* Contains the manual \`eventsList\` filtering logic (where the
\`locationName\` check was added).

\* Manages the filter state for the entire list.

2\.
\*\*\[EventFiltersModal.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/events/EventFiltersModal.tsx)\*\*:

\* Manages the UI for selecting categories, timeframe, and searching for
locations.

\* Handles the autocomplete logic for cities.

3\.
\*\*\[EventListBottomSheet.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/events/EventListBottomSheet.tsx)\*\*:

\* Wraps the \`EventList\` in a modal/bottom-sheet layout.

\-\--

\*\*Report Status:\*\* Completed & Verified.

# Problem 108

The **Clear Search** functionality appeared broken because the UI
refused to update after the user tapped the button. Despite the backend
successfully deleting the history and the React Query cache being
cleared, the list of recent searches remained visible on the screen.

### **The Three Main Culprits:**

1.  **Stale Closures:** renderItem and renderTabContent were wrapped in
    useCallback with missing dependencies, causing them to hold onto
    \"ghost\" versions of the old search data.

2.  **FlatList Reactivity:** Since the data array reference
    (searchSections) never changed, the FlatList (a PureComponent)
    didn\'t realize it needed to re-render.

3.  **Hook Overwrites:** In the hook, spreading \...options at the
    bottom of useMutation was accidentally erasing the internal
    cache-clearing logic.

## **Core File: src/api/hooks/useSearch.ts**

### **The Fix: Mutation Logic & Cache Targeting**

We fixed the hook by moving \...options to the top and using
setQueriesData with { exact: false } to ensure we hit the query key
regardless of the limit parameter.

TypeScript

export const useClearRecentSearches = (options?: any) =\> {

const queryClient = useQueryClient();

return useMutation({

\...options, // Spread first to avoid overwriting logic below

mutationFn: clearRecentSearches,

onMutate: async (variables) =\> {

// 1. Cancel outgoing fetches to prevent race conditions

await queryClient.cancelQueries({ queryKey: queryKeys.search.recent });

// 2. Optimistic update: Target fuzzy keys (exact: false) to catch keys
like \[\'recent\', 4\]

queryClient.setQueriesData({ queryKey: queryKeys.search.recent, exact:
false }, () =\> \[\]);

return { /\* context \*/ };

},

onSuccess: async () =\> {

// 3. Final sync with the server

await queryClient.invalidateQueries({ queryKey: queryKeys.search.recent
});

}

});

};

## **Core File: src/screens/search/Search.tsx**

### **The Fix 1: Removing Stale Closures**

We removed the useCallback wrappers from the render functions. This
ensures that every time the component re-renders with new data, the
functions are fresh and have access to the latest recentSearchesData.

TypeScript

// Removed useCallback to prevent stale closure \"time-travel\"

const renderTabContent = () =\> {

if (!hasQueryText && recentSearchesData?.length \> 0) {

return (

\<RecentSearchesList

data={recentSearchesData} // Now guaranteed to be fresh

onClear={clearSearchHistory}

onItemPress={setSearchQuery}

/\>

);

}

// \... rest of logic

};

### **The Fix 2: FlatList Reactivity with extraData**

We added the extraData prop to the FlatList. This tells the list:
*\"Even if your main \'data\' array looks the same, you must re-render
if any of these variables change.\"*

TypeScript

\<FlatList

data={searchSections}

// The \"Reactivity Bridge\"

extraData={\[recentSearchesData, searchData, activeTab, searchQuery\]}

renderItem={renderItem}

keyExtractor={item =\> item.id}

// \... rest of props

/\>

## **Key Takeaways for Future Reference**

- **The Overwrite Rule:** Always spread options at the *top* of a custom
  hook\'s internal logic, or manually fire the callbacks
  (options.onSuccess()) to ensure both the hook and the component logic
  run.

- **The FlatList ExtraData Rule:** If your list items depend on state
  that isn\'t inside the data prop (like a theme or a separate API
  hook), you **must** use extraData.

- **The Callback Trap:** useCallback is great for performance but
  dangerous for data-heavy renders. If a list isn\'t updating, the first
  step is to strip the useCallback and check if the closure was stale.

- **Fuzzy Matching:** When using React Query keys with variables (like
  limit or id), use { exact: false } in setQueriesData to wipe all
  variations of that key at once.

# Problem 109

\*\*Type\*\*: \`Render Error\`

\*\*Message\*\*: \`locationSearch.trim is not a function (it is
undefined)\`

\*\*Cause\*\*: The \`locationSearch\` state variable in
\`JobFiltersModal.tsx\` was unexpectedly becoming \`null\` or
\`undefined\`. This typically occurs during component re-renders or when
props are updated before the state has synchronized, causing the call to
\`.trim()\` to crash the app.

\#### 2. Important Code Snippets

\*\*The Fix (Defensive Programming)\*\*:

To prevent the crash, I added safety checks to ensure \`locationSearch\`
exists and is a string before performing any operations on it.

\`\`\`tsx

// Inside filteredLocations useMemo

const filteredLocations = React.useMemo(() =\> {

if (!availableLocations) return \[\];

// Safety check added here

if (!locationSearch \|\| typeof locationSearch !== \'string\' \|\|
!locationSearch.trim()) {

return availableLocations;

}

return availableLocations.filter(loc =\>

loc.label.toLowerCase().includes(locationSearch.toLowerCase())

);

}, \[availableLocations, locationSearch\]);

// Inside the render block

{locationSearch &&

typeof locationSearch === \'string\' &&

locationSearch.trim().length \> 0 &&

filteredLocations.length \> 0 && (

\<View style={styles.chipContainer}\>

{/\* \... \*/}

\</View\>

)}

\`\`\`

\#### 3. Files Involved

\- \*\*Logic & UI Fix\*\*:
\`src/screens/job_portal/components/JobFiltersModal.tsx\`

\- \*\*Translations\*\*:

\- \`src/i18n/locales/en.json\`

\- \`src/i18n/locales/es.json\`

\- \`src/i18n/locales/fr.json\`

\#### 4. Additional UI Improvements Made

\- \*\*Button Alignment\*\*: Fixed the \'Reset\' and \'Apply\' buttons
in the modal footer by wrapping them in \`flex: 1\` containers to ensure
equal width.

\- \*\*Safe Area Support\*\*: Updated the footer padding to use
\`useSafeAreaInsets()\` to prevent buttons from being cut off on devices
with home indicators (e.g., iPhone 15, newer Androids).

# Problem 110

When a new event was created on the CreateEvent screen, it did not
immediately appear on the parent Events screen (in the \"Upcoming
Events\" or \"Other Events\" lists) after navigating back.

This was a **React Query cache invalidation issue**. The lists on the
parent screen fetch their data using the queryKeys.events.eventList base
key. However, the useCreateEvent mutation was only invalidating the
queryKeys.events.events key upon a successful creation. Because the
specific eventList cache wasn\'t cleared or marked as stale, React Query
continued to serve the old cached data instead of fetching the updated
list from the server.

### **📄 File Name**

src/api/hooks/useEvents.ts

### **💻 The Solution (Code Snippet)**

The fix required explicitly adding a cache invalidation for the
eventList query key inside the onSuccess callback of the useCreateEvent
mutation.

TypeScript

export const useCreateEvent = () =\> {

return useMutation({

mutationKey: queryKeys.events.createEvent,

mutationFn: (payload: any) =\> createEvent(payload),

onSuccess: () =\> {

// 1. Invalidates the general events cache (Existing)

queryClient.invalidateQueries({

queryKey: queryKeys.events.events,

refetchType: \'all\',

});

// 2. ADDED: Invalidates the specific event lists used on the Events
screen

queryClient.invalidateQueries({

queryKey: queryKeys.events.eventList,

refetchType: \'all\',

});

},

});

};

### **🧠 Why it works**

By invalidating queryKeys.events.eventList, you force React Query to
mark the cached arrays for both useGetEvents and useEventsInfiniteQuery
as stale. When you navigate back to the Events screen, React Query sees
the stale data flag and instantly triggers a background fetch, pulling
the fresh data (including your new event) and updating the UI
automatically.

# Problem 111

\# Debugging Report: Empty Job Type Modal Issue

\## 1. Problem Description

In the \*\*New Opportunity\*\* (Create Job) screen, clicking on the
\*\*Job Type\*\* field opened a modal that appeared empty (rows were
selectable but displayed no text). This prevented users from selecting a
job type.

\## 2. Root Cause Analysis

\### A. Incorrect API Endpoint

The \`EMPLOYMENT_TYPE\` key in the centralized API configuration was
pointing to the wrong autocomplete endpoint. Instead of fetching
employment types (Full-time, Part-time), it was fetching work
arrangements (Remote, On-site).

\* \*\*File\*\*: \`src/api/endpoints.ts\`

\* \*\*Incorrect Code\*\*:

\`\`\`typescript

EMPLOYMENT_TYPE: (query: string) =\>
\`/autocomplete/work-arrangement?q=\${encodeURIComponent(query)}\`,

\`\`\`

\* \*\*Impact\*\*: The app requested data from the wrong backend table.

\### B. Rigid Data Mapping

The \`EmploymentType\` service was strictly mapping a field named
\`type_name\` to the UI \`label\`. Because the wrong endpoint was being
hit, the returned objects contained \`arrangement_type\` instead of
\`type_name\`, resulting in an undefined label.

\* \*\*File\*\*: \`src/api/services/autcomplete.service.ts\`

\* \*\*Old Mapping\*\*:

\`\`\`typescript

label: item?.type_name ?? \'\',

\`\`\`

\* \*\*Impact\*\*: The UI rendered rows with empty strings as text.

\## 3. Implementation Details

\### File 1: Correcting the Endpoint

\*\*File\*\*:
\[endpoints.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/api/endpoints.ts)

\`\`\`diff

\- EMPLOYMENT_TYPE: (query: string) =\>
\`/autocomplete/work-arrangement?q=\${encodeURIComponent(query)}\`,

\+ EMPLOYMENT_TYPE: (query: string) =\>
\`/autocomplete/employment-type?q=\${encodeURIComponent(query)}\`,

\`\`\`

\### File 2: Robust Service Mapping

\*\*File\*\*:
\[autcomplete.service.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/api/services/autcomplete.service.ts)

\`\`\`diff

\- label: item?.type_name ?? \'\',

\+ // Robust mapping with fallbacks for better API compatibility

\+ label: item?.type_name ?? item?.name ?? item?.label ?? \'\',

\`\`\`

\### File 3: Standardizing i18n

The \"Work Arrangement\" field was also found to be using hardcoded
strings, which was fixed to follow project standards.

\*\*File\*\*:
\[CreateJob.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/job_portal/CreateJob.tsx)

\`\`\`diff

\- label: \'Work Arrangement\',

\- placeholder: \'Select work arrangement\',

\- rules: { required: \'Work arrangement is required\' },

\+ label: t(\'jobPortal.create.form.workArrangementLabel\'),

\+ placeholder: t(\'jobPortal.create.form.workArrangementPlaceholder\'),

\+ rules: { required:
t(\'jobPortal.create.validation.workArrangementRequired\') },

\`\`\`

\## 4. Summary of Resolution

By correcting the endpoint URL and adding fallbacks to the data mapper,
the \*\*Job Type\*\* modal now correctly retrieves and displays data
from the backend. The integration of \`i18n\` for the \"Work
Arrangement\" field ensures the screen is fully localized and follows
the project\'s coding standards.

# Problem 112

\# User-Friendly Time Formatting for Jobs postings and expiration date

The goal is to improve the time format for job posting dates and
expiration dates. Within 24 hours, time should be relative (e.g., \"30
mins ago\", \"2 hours ago\"). Beyond 24 hours, it should show days
(e.g., \"1 day ago\", \"2 days ago\").

\## User Review Required

\> \[!IMPORTANT\]

\> The current \"Added Today\" and \"Added Yesterday\" in
\`JobOpportunities.tsx\` will be replaced by more granular relative
times (mins/hours ago) if within 24 hours.

\## Proposed Changes

\### Internationalization

\#### \[MODIFY\]
\[en.json\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/i18n/locales/en.json)

Add new keys for relative time in \`homeComponents\`:

\- \`justNow\`: \"just now\"

\- \`minsAgo\`: \"{{count}} mins ago\"

\- \`hoursAgo\`: \"{{count}} hours ago\"

\- \`daysAgo\`: \"{{count}} days ago\" (updating existing if needed)

\- \`expiringInMins\`: \"Expiring in {{count}} mins\"

\- \`expiringInHours\`: \"Expiring in {{count}} hours\"

\- \`expiringInDays_one\`: \"Expiring in {{count}} day\"

\- \`expiringInDays_other\`: \"Expiring in {{count}} days\"

\### Utils

\#### \[MODIFY\]
\[helpers.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/utils/helpers.ts)

Implement \`getRelativeTime\` and \`getExpiryTime\` functions.

\`\`\`typescript

export const getRelativeTime = (date: Date \| string, t: any): string
=\> {

const now = new Date();

const past = new Date(date);

const diffMs = now.getTime() - past.getTime();

const diffSecs = Math.floor(diffMs / 1000);

const diffMins = Math.floor(diffSecs / 60);

const diffHours = Math.floor(diffMins / 60);

const diffDays = Math.floor(diffHours / 24);

if (diffMins \< 1) return t(\'homeComponents.justNow\');

if (diffMins \< 60) return t(\'homeComponents.minsAgo\', { count:
diffMins });

if (diffHours \< 24) return t(\'homeComponents.hoursAgo\', { count:
diffHours });

if (diffDays === 1) return t(\'homeComponents.yesterday\');

if (diffDays \< 7) return t(\'homeComponents.daysAgo\', { count:
diffDays });

// Return formatted date for anything older than a week

return past.toLocaleDateString(\'en-US\', {

year: \'numeric\',

month: \'short\',

day: \'numeric\',

});

};

export const getExpiryTime = (date: Date \| string, t: any): string =\>
{

const now = new Date();

const target = new Date(date);

const diffMs = target.getTime() - now.getTime();

const diffSecs = Math.floor(diffMs / 1000);

const diffMins = Math.floor(diffSecs / 60);

const diffHours = Math.floor(diffMins / 60);

const diffDays = Math.ceil(diffHours / 24);

if (diffMs \<= 0) return t(\'homeComponents.expired\');

if (diffMins \< 60) return t(\'homeComponents.expiringInMins\', { count:
diffMins });

if (diffHours \< 24) return t(\'homeComponents.expiringInHours\', {
count: diffHours });

return t(\'homeComponents.expiringInDays\', { count: diffDays });

};

\`\`\`

\### Components

\#### \[MODIFY\]
\[JobOpportunities.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/home/JobOpportunities.tsx)

\- Remove local \`formatTimeSince\` and \`getDaysRemaining\`.

\- Update \`renderJobItem\` to use the new helper functions.

\#### \[MODIFY\]
\[JobDetails.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/job_portal/JobDetails.tsx)

\- Update the \"Posted\" and \"Expires in\" text to use the new helpers.

\#### \[MODIFY\]
\[JobPostings.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/job_portal/JobPostings.tsx)

\- Update the job list items to show relative time for
\`publicationDate\`.

\## Verification Plan

\### Automated Tests

\- I will check for Text string errors and VirtualizedList errors as
requested.

\### Manual Verification

\- Verify the \"Added Today\" changes to \"X mins ago\" or \"X hours
ago\".

\- Verify \"Expiring in 1 day\" still works and shows hours/mins if
closer.

\- Verify consistency across all job-related screens.

# Problem 113

\#### 1. The Problem

There were three distinct but overlapping issues occurring
simultaneously when clicking the \"Join\" button on Recommended
Community cards:

\* \*\*Event Propagation:\*\* The \"Join\" button was nested inside a
navigation-triggered card. Clicking \"Join\" would simultaneously
trigger a background API call AND a full-screen navigation transition.

\* \*\*Global Skeleton Aggression:\*\* In \`Home.tsx\`, the logic for
showing the skeleton loader was too sensitive. Any background data fetch
(even for refreshing existing data) would trigger the full-screen
\`HomeScreenSkeletonLoader\`, making the app appear to \"reset\" or
\"return to Home.\"

\* \*\*State Reset on Remount:\*\* Because the skeleton loader was
replacing the entire screen, the \`RecommendedCommunities\` component
was being unmounted and remounted. This caused any local loading states
(like the button changing to \"Joined\") to be lost before the API
refetch completed.

\-\--

\#### 2. Key Files Modified

\| File Name \| Responsibility \|

\| :\-\-- \| :\-\-- \|

\|
\[Home.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/founder/home/Home.tsx)
\| Managed global loading/skeleton states for the Home dashboard. \|

\|
\[RecommendedCommunities.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/community/components/community-dashboard/TabScreen/components/RecommendedCommunities.tsx)
\| Rendered the community cards and handled the \"Join\" mutation. \|

\-\--

\#### 3. Important Code Snippets

\*\*A. Refined Skeleton Logic
(\[Home.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/founder/home/Home.tsx))\*\*

We changed the logic from a global check to a section-specific check.
The skeleton now only appears if a section is \*\*fetching AND has no
data in cache\*\*.

\`\`\`tsx

// Before: showSkeleton = !isTransitionFinished \|\|
(isAnySectionMissingData && isDataFetching);

// After:

const showSkeleton =

!isTransitionFinished \|\|

(trendingFetching \> 0 && !trendingHasData) \|\|

(eventsFetching \> 0 && !eventsHasData) \|\|

(jobsFetching \> 0 && !jobsHasData) \|\|

(mentorsFetching \> 0 && !mentorsHasData) \|\|

(communitiesFetching \> 0 && !communitiesHasData);

\`\`\`

\*\*B. Decoupled Touchable Logic
(\[RecommendedCommunities.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/community/components/community-dashboard/TabScreen/components/RecommendedCommunities.tsx))\*\*

We moved the Join button outside of the main navigation
\`TouchableOpacity\` to prevent event collision.

\`\`\`tsx

\<View style={styles.cardContainer}\>

{/\* Card Content (Navigation Only) \*/}

\<TouchableOpacity onPress={() =\> handleNavigation(community)}\>

\<View\>{/\* Avatar and Title \*/}\</View\>

\</TouchableOpacity\>

{/\* Join Button (Mutation Only) \*/}

\<TouchableOpacity onPress={() =\> handleJoin(community.id)}\>

\<Text\>{isJoined ? \'Joined\' : \'Join\'}\</Text\>

\</TouchableOpacity\>

\</View\>

\`\`\`

\*\*C. Local Join State
(\[RecommendedCommunities.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/community/components/community-dashboard/TabScreen/components/RecommendedCommunities.tsx))\*\*

We added a local state to ensure the button remains in the \"Joined\"
state even during the transition period before the API list is
refreshed.

\`\`\`tsx

const \[locallyJoinedIds, setLocallyJoinedIds\] =
React.useState\<string\[\]\>(\[\]);

// In render:

const isJoined = community.isMember \|\|
locallyJoinedIds.includes(community.id);

\`\`\`

\-\--

\#### 4. Future Reference

If a similar \"Flicker\" or \"Reset\" issue occurs on other screens:

1\. Check the \*\*Skeleton Logic\*\*: Ensure background refetches (where
data already exists) do not trigger full-screen loaders.

2\. Check for \*\*Nested Touchables\*\*: Ensure buttons inside cards are
siblings, not children, of the card\'s touchable area.

3\. Check \*\*Query Invalidation\*\*: Remember that
\`invalidateQueries\` triggers a fetch that \`useIsFetching\` will pick
up.

# Problem 114

\# Walkthrough - Mentorship Navigation Fix

I have resolved the issue where clicking \"Mentorship → View All\"
incorrectly redirected to the Search page. I have created a dedicated
mentors listing page and updated all necessary navigation and
internationalization logic.

\## Changes Made

\### 1. Navigation Setup

\- Added \`MENTOR_LIST\` to \`SCREEN_NAMES\` in
\[navigation.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/constants/navigation.ts).

\- Registered the new \`MentorList\` screen in
\[AppNavigator.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/navigation/AppNavigator.tsx).

\- Added \`MENTOR_LIST\` to the \`RootStackParamList\` in
\[types/navigation.ts\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/types/navigation.ts).

\### 2. New Mentors Screen

\- Created a dedicated
\[MentorList.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/mentor/MentorList.tsx)
screen.

\- Implemented a search bar and a scrollable list of mentors.

\- Included lazy loading support in
\[index.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/mentor/index.tsx).

\### 3. Component Updates

\- Updated the \"View All\" action in
\[Mentorship.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/home/Mentorship.tsx)
to point to the new screen.

\- Internationalized hardcoded strings like \"Connect\" and \"Expert
Mentor\".

\### 4. Internationalization

\- Added new translation keys for the Mentors screen and actions in
\[en.json\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/i18n/locales/en.json).

\## Verification Results

\### Manual Verification

\- Navigating from Home to \"Mentorship → View All\" now correctly opens
the \*\*Mentors\*\* listing page.

\- The search functionality on the Mentors page allows filtering by name
and profession.

\- The \"Connect\" button and avatar press correctly navigate to the
mentor\'s profile.

\- All strings are now properly translated via \`i18next\`.

\-\--

\*\*⚠️ Hygiene Check\*\*:

\- Verified that no \`VirtualizedList\` nesting errors were introduced.

\- Verified that all text strings are rendered within \`\<Text\>\`
components.

# Problem 115

\# Walkthrough - Scroll-to-Hide Header in ChatBot

I have implemented the requested scroll-to-hide behavior for the header
in the ChatBot screen, matching the logic found in the Home screen.

\## Changes Made

\### 1. Updated \`TopHeader.tsx\`

\- Converted the main container to \`Animated.View\` to support
animations.

\- Added \`isAbsolute\` and \`animatedStyle\` props for flexible usage.

\- Updated styles to support absolute positioning and safe area insets
when absolute.

\- Ensured backward compatibility: existing headers remain relative and
non-animated by default.

\### 2. Enhanced \`ChatBotScreen.tsx\`

\- Integrated \`react-native-reanimated\` to handle scroll animations.

\- Implemented \`useAnimatedScrollHandler\` to hide the header when
scrolling down and show it when scrolling up.

\- Replaced \`FlatList\` with \`Animated.FlatList\`.

\- Passed the animation logic to \`TopHeader\`.

\- Adjusted the layout (skeleton and main view) to account for the
absolute header positioning.

\## Verification Results

\### Automated Checks

\- \*\*Stray Strings\*\*: Scanned \`ChatBotScreen.tsx\`, no stray
strings found.

\- \*\*VirtualizedList Nesting\*\*: Scanned \`ChatBotScreen.tsx\`, no
nested \`FlatList\` inside \`ScrollView\` found.

\### Manual Verification (Simulation)

\- Header height calculated as \`56 + insets.top\`.

\- Scroll down: Header translates by \`-headerHeight\` (fully hidden).

\- Scroll up: Header translates back to \`0\` (visible).

\- Top of list: Header remains visible.

\## Files Modified

\-
\[TopHeader.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/components/common/TopHeader.tsx)

\-
\[ChatBotScreen.tsx\](file:///Users/victorloucii/Nexteir_Technologies/CHHIRO_COMMUNITY_MOBILE_APP/src/screens/chat_bot/ChatBotScreen.tsx)
