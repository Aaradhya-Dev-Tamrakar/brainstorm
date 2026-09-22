import fs from "fs";
import path from "path";

const tools = [
  {
    name: "list_courses",
    description: "List courses where the user is a student or teacher (e.g. active or archived classes).",
    parameters: {
      type: "object",
      properties: {
        courseStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter by states: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED. Defaults to ['ACTIVE']."
        },
        pageSize: { type: "number", description: "Maximum number of courses to return (default 20)." },
        studentId: { type: "string", description: "Filter courses enrolled as student (e.g. 'me')." },
        teacherId: { type: "string", description: "Filter courses taught as teacher (e.g. 'me')." }
      }
    }
  },
  {
    name: "get_course",
    description: "Get detailed information about a specific course by Course ID.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." }
      },
      required: ["courseId"]
    }
  },
  {
    name: "list_coursework",
    description: "List assignments, quizzes, and coursework for a specific course.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter by states: PUBLISHED, DRAFT, DELETED. Defaults to ['PUBLISHED']."
        },
        pageSize: { type: "number", description: "Maximum number of assignments to return (default 30)." },
        orderBy: { type: "string", description: "Sort order, e.g., 'dueDate desc' or 'updateTime desc'." }
      },
      required: ["courseId"]
    }
  },
  {
    name: "get_coursework",
    description: "Get detailed information for a specific assignment, including description, attached Drive files, YouTube links, and rubrics.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkId: { type: "string", description: "The unique identifier of the coursework." }
      },
      required: ["courseId", "courseWorkId"]
    }
  },
  {
    name: "list_submissions",
    description: "List student submissions for a coursework (status: TURNED_IN, RETURNED, NEW, late status, assigned grade).",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkId: { type: "string", description: "The coursework identifier (or '-' for all coursework in the course)." },
        userId: { type: "string", description: "Optional student filter ('me' for current user, or student user ID)." },
        states: {
          type: "array",
          items: { type: "string" },
          description: "Filter by submission states: NEW, CREATED, TURNED_IN, RETURNED, RECLAIMED_BY_STUDENT."
        },
        pageSize: { type: "number", description: "Maximum number of submissions to return." }
      },
      required: ["courseId", "courseWorkId"]
    }
  },
  {
    name: "get_submission",
    description: "Get detailed student submission info including attached files, links, and assigned grade.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkId: { type: "string", description: "The coursework identifier." },
        submissionId: { type: "string", description: "The submission ID." }
      },
      required: ["courseId", "courseWorkId", "submissionId"]
    }
  },
  {
    name: "list_announcements",
    description: "List stream announcements, notices, and updates for a course.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        announcementStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter states: PUBLISHED, DRAFT, DELETED. Defaults to ['PUBLISHED']."
        },
        pageSize: { type: "number", description: "Maximum number of announcements to return (default 20)." },
        orderBy: { type: "string", description: "Sort order, e.g. 'updateTime desc'." }
      },
      required: ["courseId"]
    }
  },
  {
    name: "list_coursework_materials",
    description: "List materials, syllabi, lecture slides, and resources posted under Classwork.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkMaterialStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter states: PUBLISHED, DRAFT, DELETED. Defaults to ['PUBLISHED']."
        },
        pageSize: { type: "number", description: "Maximum number of materials to return (default 20)." }
      },
      required: ["courseId"]
    }
  },
  {
    name: "list_teachers",
    description: "List teachers of a course.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        pageSize: { type: "number", description: "Max teachers to return." }
      },
      required: ["courseId"]
    }
  },
  {
    name: "list_students",
    description: "List students enrolled in a course.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        pageSize: { type: "number", description: "Max students to return." }
      },
      required: ["courseId"]
    }
  },
  {
    name: "turn_in_assignment",
    description: "Turn in a student submission for grading.",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The course ID." },
        courseWorkId: { type: "string", description: "The coursework ID." },
        submissionId: { type: "string", description: "The submission ID." }
      },
      required: ["courseId", "courseWorkId", "submissionId"]
    }
  },
  {
    name: "reclaim_assignment",
    description: "Reclaim a turned-in student submission (unsubmit).",
    parameters: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The course ID." },
        courseWorkId: { type: "string", description: "The coursework ID." },
        submissionId: { type: "string", description: "The submission ID." }
      },
      required: ["courseId", "courseWorkId", "submissionId"]
    }
  }
];

const targetDir = path.join(
  process.env.USERPROFILE || process.env.HOME || "",
  ".gemini",
  "antigravity",
  "mcp",
  "classroom"
);

if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
}

for (const tool of tools) {
  const filePath = path.join(targetDir, `${tool.name}.json`);
  fs.writeFileSync(filePath, JSON.stringify(tool, null, 2));
  console.log(`Wrote schema: ${filePath}`);
}

console.log(`\nSuccessfully synced ${tools.length} classroom MCP tool schemas to ${targetDir}`);
