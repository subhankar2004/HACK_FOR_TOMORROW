# 🚀 HACK FOR TOMORROW - Guidelines & Instructions

Welcome to the official repository for **HACK FOR TOMORROW**! 🎉

## 📌 Overview
This repository serves as the global codebase for all participating teams. Each team will have a designated folder where they will fork the repo push their code updates daily via pull requests (PRs).

## 📁 Repository Structure
```
📦 hackathon-repo
 ┣ 📂 team-name-1
 ┃ ┣ 📜 README.md
 ┃ ┗ 📂 src/
 ┣ 📂 team-name-2
 ┃ ┣ 📜 README.md
 ┃ ┗ 📂 src/
 ┗ ...
```
Each team will be assigned a folder named after their **team name** inside the repository.

---

## 📥 Getting Started
Follow these steps to clone the repository and start working:

**Fork the repo**

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/YOUR_ORG/HACK-FOR-TOMORROW.git
 cd HACK-FOR-TOMORROW
```

### 2️⃣ Create Your Team Folder
Navigate inside the repo and create a new folder using your **team name** (if not already created):
```bash
 mkdir your-team-name
 cd your-team-name
```

### 3️⃣ Add Your Code
Place your source code and assets inside your team's folder. Maintain a structured format.

### 4️⃣ Commit and Push Changes
#### ⚡ Step 1: Add your changes
```bash
 git add .
```
#### ⚡ Step 2: Commit with a meaningful message
```bash
 git commit -m "[Team Name] - Added initial project setup"
```
#### ⚡ Step 3: Push your changes
```bash
 git push origin main
```

---

## 🔄 Submitting Daily Updates (Pull Requests)
At the end of each day, submit a **pull request (PR)** with your updates:

### 1️⃣ Pull the latest changes from the repository
```bash
 git pull origin main
```
### 2️⃣ Create a new branch with your team name
```bash
 git checkout -b your-team-name-update
```
### 3️⃣ Push your branch to GitHub
```bash
 git push origin your-team-name-update
```
### 4️⃣ Create a Pull Request
- Go to the GitHub repository.
- Click on **New Pull Request**.
- Select **your-team-name-update** as the source branch.
- Add a meaningful description of your progress.
- Submit the PR for review.

---

## ⚠️ Rules & Best Practices
✅ Commit frequently and use meaningful commit messages.
✅ Keep your code organized inside your team folder.
✅ Do not modify files outside your team folder.
✅ Follow the deadline for PR submissions every day.
✅ Resolve merge conflicts properly before pushing.
✅ No plagiarism or direct copy-pasting of code from the internet.

---

## ❓ Need Help?
If you have any questions or face issues, contact the hackathon organizers via **Our Volunteers**.

Happy Coding! 🎯🚀
