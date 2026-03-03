# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
mark field in POST /students is optional but does not define what happens if the field is omitted.
2) How you have accounted for this in your implementation
if mark is not provided in the request body, my implementation will default it to 0. This ensures a student can still be created successfully even if the mark is not provided, and the database always stores a valid integer for mark.