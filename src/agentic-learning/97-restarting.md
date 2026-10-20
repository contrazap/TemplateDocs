## Restarting an existing workspace

When a workspace built another way switches to this template and the user wants to build along from the start:

1. Agree with the user what is kept: documents, design, decisions still valid. If the user wants the old code kept, tag or archive it; otherwise remove it. Records may start fresh.
2. Inventory what the agent installed earlier (tools, SDK templates, browser or package caches, containers, images and volumes, repository hooks and settings files) and what the user installed. With the user's authorization, uninstall what the agent installed, stopping processes that hold files first. Keep what the user installed.
3. Confirm the clean state with the commands the steps will later use as 📋 Before (for example an empty tool list), so each reinstall shows a visible before and after.
4. Write the first plan's overview and first step, starting from the repository basics a developer would set up first.
