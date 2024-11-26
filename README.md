# Bone Renamer Addon for Blender
The Bone Renamer Addon is a powerful tool for Blender that allows you to rename multiple bones in an armature using a JSON file. This addon provides a user-friendly interface to load, edit, and save bone mappings, making it easier to manage and apply bone name changes.

## Features
**Load Bone Mappings**: Load bone mappings from a JSON file.

Save Bone Mappings: Save the current bone mappings to a JSON file.

Add Bone Mapping: Add new bone mappings manually.

Remove Bone Mapping: Remove existing bone mappings.

Swap Bone Mappings: Swap the old and new names of bone mappings.

Move Bone Mapping: Move bone mappings up and down in the list.

Clear Bone Mappings: Clear the current list of bone mappings.

Load Armature Bones: Load the selected armature's bones into the source list.

Rename Bones: Rename bones based on the loaded mappings.


## Usage
Open the Addon Panel:

1. Go to the 3D Viewport.

  Open the Tool panel (if not visible, press N to toggle the sidebar).
  You should see a new panel called Bone Renamer.

2. Select the Target Armature:

  Select the Target Armature from the dropdown menu in the Bone Renamer panel.

3. Load Bone Mappings:

  Click Load JSON File to load your JSON file containing bone mappings.

4. Edit Bone Mappings:

  You can edit the new names, select/deselect bones, add new mappings, and remove existing mappings.
  
  Use the up and down arrows to move bone pairs up and down in the list.
  
  Click Swap Bone Mappings to swap the old and new names.
  
  Click Clear List to clear the current list.
  
  Click Load Armature Bones to load the selected armature's bones into the source list.

5. Save Bone Mappings:

  Click Save JSON File to save the current list to a JSON file.

6. Rename Bones:

  Click Rename Bones to commit the changes to the selected armature. If there is no list loaded, the "Rename Bones" button will be disabled.
