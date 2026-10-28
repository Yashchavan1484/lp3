// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title Student data using Structures, Arrays and a Fallback function
contract StudentData {
    struct Student {
        uint256 rollNo;
        string name;
        uint8 age;
        string course;
    }

    Student[] public students; // dynamic array of structs

    event StudentAdded(uint256 indexed rollNo, string name);
    event FallbackCalled(address indexed sender, uint256 value, bytes data);

    // Add a new student
    function addStudent(
        uint256 _rollNo,
        string memory _name,
        uint8 _age,
        string memory _course
    ) public {
        students.push(Student(_rollNo, _name, _age, _course));
        emit StudentAdded(_rollNo, _name);
    }

    // Get a student by array index
    function getStudent(uint256 index)
        public
        view
        returns (uint256, string memory, uint8, string memory)
    {
        require(index < students.length, "Index out of range");
        Student memory s = students[index];
        return (s.rollNo, s.name, s.age, s.course);
    }

    // Total number of students
    function getStudentCount() public view returns (uint256) {
        return students.length;
    }

    // Fallback: runs when a non-existent function is called (or data is sent)
    fallback() external payable {
        emit FallbackCalled(msg.sender, msg.value, msg.data);
    }

    // Receive: runs on plain ether transfers with empty calldata
    receive() external payable {
        emit FallbackCalled(msg.sender, msg.value, "");
    }
}
