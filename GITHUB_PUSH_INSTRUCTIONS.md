# GitHub Push Instructions

## Option 1: Using GitHub Desktop (Recommended for Windows Users)

1. **Download and Install GitHub Desktop**
   - Download from: https://desktop.github.com/
   - Install and sign in with your GitHub account

2. **Add the Local Repository**
   - In GitHub Desktop, click on "File" > "Add local repository"
   - Browse to `C:\Users\RAJ\Desktop\h1` and select it
   - If prompted that this directory is not a repository, click on "create a repository"

3. **Push to GitHub**
   - Give your repository a name (e.g., "fake-news-detection")
   - Add a description (optional)
   - Keep "Local Path" as is
   - Choose whether to make it Public or Private
   - Click "Create repository"
   - Click "Publish repository"

## Option 2: Using Git with Personal Access Token (PAT)

1. **Create a Personal Access Token on GitHub**
   - Go to GitHub: https://github.com
   - Click on your profile picture in the top-right corner
   - Select "Settings"
   - Scroll down to "Developer settings" (at the bottom of the left sidebar)
   - Select "Personal access tokens" and then "Tokens (classic)"
   - Click "Generate new token" (classic)
   - Give it a descriptive name (e.g., "Fake News Detection Project")
   - Select the necessary scopes (at minimum, select "repo" for full control of repositories)
   - Click "Generate token"
   - Copy the token immediately (you won't be able to see it again)

2. **Create a New Repository on GitHub**
   - Go to GitHub: https://github.com
   - Click on the "+" icon in the top-right corner and select "New repository"
   - Repository name: `fake-news-detection`
   - Description: `A web application for analyzing and detecting fake news using machine learning`
   - Choose Public or Private
   - Do NOT initialize with any files
   - Click "Create repository"

3. **Push Your Code**
   - Open PowerShell or Command Prompt
   - Navigate to your project folder:
     ```
     cd C:\Users\RAJ\Desktop\h1
     ```
   - Set the remote URL with your token:
     ```
     git remote set-url origin https://YOUR-USERNAME:YOUR-TOKEN@github.com/YOUR-USERNAME/fake-news-detection.git
     ```
     (Replace `YOUR-USERNAME` with your GitHub username and `YOUR-TOKEN` with the token you created)
   - Push your code:
     ```
     git push -u origin main
     ```

## Option 3: Using SSH Authentication

1. **Generate an SSH Key**
   - Open PowerShell or Command Prompt
   - Run:
     ```
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```
   - Press Enter to accept the default file location
   - Enter a secure passphrase (or press Enter for no passphrase)

2. **Add the SSH Key to the SSH Agent**
   - Start the SSH agent:
     ```
     eval "$(ssh-agent -s)"
     ```
   - Add your key:
     ```
     ssh-add ~/.ssh/id_ed25519
     ```

3. **Add the SSH Key to Your GitHub Account**
   - Copy the SSH key to clipboard:
     ```
     cat ~/.ssh/id_ed25519.pub | clip
     ```
   - Go to GitHub: https://github.com
   - Click on your profile picture > Settings
   - Select "SSH and GPG keys" from the sidebar
   - Click "New SSH key"
   - Give it a title (e.g., "Personal Laptop")
   - Paste the key into the "Key" field
   - Click "Add SSH key"

4. **Create a New Repository on GitHub**
   - Go to GitHub: https://github.com
   - Click on the "+" icon in the top-right corner and select "New repository"
   - Repository name: `fake-news-detection`
   - Description: `A web application for analyzing and detecting fake news using machine learning`
   - Choose Public or Private
   - Do NOT initialize with any files
   - Click "Create repository"

5. **Push Your Code**
   - Open PowerShell or Command Prompt
   - Navigate to your project folder:
     ```
     cd C:\Users\RAJ\Desktop\h1
     ```
   - Update the remote URL to use SSH:
     ```
     git remote set-url origin git@github.com:YOUR-USERNAME/fake-news-detection.git
     ```
     (Replace `YOUR-USERNAME` with your GitHub username)
   - Push your code:
     ```
     git push -u origin main
     ``` 