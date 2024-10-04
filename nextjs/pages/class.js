import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  TextField,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { useRouter } from "next/router";

// Class Page Component
const Classroom = () => {
  const [className, setClassName] = useState(""); // For the new class name input
  const [classes, setClasses] = useState([]); // To store and display fetched classes
  const router = useRouter();

  // Function to fetch existing classes from the API
  const fetchClasses = async () => {
    try {
      const response = await fetch("/api/classes"); // Modify this to match your API route
      const data = await response.json();
      setClasses(data);
    } catch (error) {
      console.error("Error fetching classes:", error);
    }
  };

  // Function to add a new class
  const handleAddClass = async () => {
    try {
      const response = await fetch("/api/classes/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ class_name: className }),
      });
      const newClass = await response.json();
      setClasses((prevClasses) => [...prevClasses, newClass]); // Add the new class to the list
      setClassName(""); // Reset input field
    } catch (error) {
      console.error("Error adding class:", error);
    }
  };

  // Function to delete a class
  const handleDeleteClass = async (classId) => {
    try {
      await fetch(`/api/classes/${classId}`, {
        method: "DELETE",
      });
      // Remove the deleted class from the list
      setClasses(classes.filter((classItem) => classItem.class_id !== classId));
    } catch (error) {
      console.error("Error deleting class:", error);
    }
  };

  // Fetch classes on page load
  useEffect(() => {
    fetchClasses();
  }, []);

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "20px",
      }}
    >
      {/* Title */}
      <Typography variant="h4" sx={{ marginBottom: "20px" }}>
        Google Classroom-like Page
      </Typography>

      {/* Form to Add a New Class */}
      <Paper sx={{ padding: "20px", marginBottom: "20px", width: "100%", maxWidth: "600px" }}>
        <Typography variant="h6" gutterBottom>
          Add a New Class
        </Typography>
        <TextField
          fullWidth
          label="Class Name"
          variant="outlined"
          value={className}
          onChange={(e) => setClassName(e.target.value)}
          sx={{ marginBottom: "16px" }}
        />
        <Button variant="contained" color="primary" fullWidth onClick={handleAddClass}>
          Add Class
        </Button>
      </Paper>

      {/* Display List of Classes */}
      <Typography variant="h6" gutterBottom>
        Your Classes
      </Typography>
      <List sx={{ width: "100%", maxWidth: "600px" }}>
        {classes.map((classItem) => (
          <Paper key={classItem.class_id} sx={{ marginBottom: "10px" }}>
            <ListItem>
              <ListItemText
                primary={classItem.class_name}
                secondary={`Created on: ${new Date(classItem.created_at).toLocaleDateString()}`}
              />
              <ListItemSecondaryAction>
                <IconButton edge="end" onClick={() => handleDeleteClass(classItem.class_id)}>
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          </Paper>
        ))}
      </List>
    </Box>
  );
};

export default Classroom;
