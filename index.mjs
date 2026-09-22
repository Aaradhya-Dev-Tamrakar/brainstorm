import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "fs";
import path from "path";

const credentialsPath =
  process.env.CLASSROOM_CREDENTIALS_PATH ||
  path.join(process.env.USERPROFILE || process.env.HOME || "", ".classroom-server-credentials.json");

const oauthPath =
  process.env.CLASSROOM_OAUTH_PATH ||
  path.join(process.env.USERPROFILE || process.env.HOME || "", ".classroom-credentials.json");

async function getAccessToken() {
  if (!fs.existsSync(credentialsPath)) {
    throw new Error(
      `Credentials file not found at ${credentialsPath}. Please run 'npm run auth' or 'node auth.mjs' first.`
    );
  }
  const creds = JSON.parse(fs.readFileSync(credentialsPath, "utf-8"));

  if (creds.access_token && creds.expiry_date && creds.expiry_date > Date.now() + 60000) {
    return creds.access_token;
  }

  if (creds.refresh_token && fs.existsSync(oauthPath)) {
    const oauth = JSON.parse(fs.readFileSync(oauthPath, "utf-8"));
    const keys = oauth.installed || oauth.web;
    const body = new URLSearchParams({
      client_id: keys.client_id,
      client_secret: keys.client_secret,
      refresh_token: creds.refresh_token,
      grant_type: "refresh_token",
    });

    const res = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });

    if (!res.ok) {
      throw new Error(`Failed to refresh token: ${await res.text()}`);
    }
    const tokenData = await res.json();
    creds.access_token = tokenData.access_token;
    if (tokenData.expires_in) {
      creds.expiry_date = Date.now() + tokenData.expires_in * 1000;
    }
    fs.writeFileSync(credentialsPath, JSON.stringify(creds, null, 2));
    return creds.access_token;
  }

  if (creds.access_token) {
    return creds.access_token;
  }

  throw new Error("No valid access token or refresh token available.");
}

async function classroomFetch(endpoint, options = {}) {
  let token = await getAccessToken();
  let headers = {
    Authorization: `Bearer ${token}`,
    Accept: "application/json",
    ...(options.headers || {}),
  };

  let url = endpoint.startsWith("http") ? endpoint : `https://classroom.googleapis.com/v1${endpoint}`;
  let res = await fetch(url, {
    ...options,
    headers,
  });

  if (res.status === 401 && fs.existsSync(credentialsPath) && fs.existsSync(oauthPath)) {
    const creds = JSON.parse(fs.readFileSync(credentialsPath, "utf-8"));
    const oauth = JSON.parse(fs.readFileSync(oauthPath, "utf-8"));
    const keys = oauth.installed || oauth.web;
    const body = new URLSearchParams({
      client_id: keys.client_id,
      client_secret: keys.client_secret,
      refresh_token: creds.refresh_token,
      grant_type: "refresh_token",
    });
    const refreshRes = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });
    if (refreshRes.ok) {
      const tokenData = await refreshRes.json();
      creds.access_token = tokenData.access_token;
      if (tokenData.expires_in) {
        creds.expiry_date = Date.now() + tokenData.expires_in * 1000;
      }
      fs.writeFileSync(credentialsPath, JSON.stringify(creds, null, 2));
      headers.Authorization = `Bearer ${creds.access_token}`;
      res = await fetch(url, {
        ...options,
        headers,
      });
    }
  }

  return res;
}

const TOOLS = [
  {
    name: "list_courses",
    description: "List courses where the user is a student or teacher (e.g. active or archived classes).",
    inputSchema: {
      type: "object",
      properties: {
        courseStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter by states: ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED. Defaults to ['ACTIVE'].",
        },
        pageSize: { type: "number", description: "Maximum number of courses to return (default 20)." },
        studentId: { type: "string", description: "Filter courses enrolled as student (e.g. 'me')." },
        teacherId: { type: "string", description: "Filter courses taught as teacher (e.g. 'me')." },
      },
    },
  },
  {
    name: "get_course",
    description: "Get detailed information about a specific course by Course ID.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
      },
      required: ["courseId"],
    },
  },
  {
    name: "list_coursework",
    description: "List assignments, quizzes, and coursework for a specific course.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter by states: PUBLISHED, DRAFT, DELETED. Defaults to ['PUBLISHED'].",
        },
        pageSize: { type: "number", description: "Maximum number of assignments to return (default 30)." },
        orderBy: { type: "string", description: "Sort order, e.g., 'dueDate desc' or 'updateTime desc'." },
      },
      required: ["courseId"],
    },
  },
  {
    name: "get_coursework",
    description: "Get detailed information for a specific assignment, including description, attached Drive files, YouTube links, and rubrics.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkId: { type: "string", description: "The unique identifier of the coursework." },
      },
      required: ["courseId", "courseWorkId"],
    },
  },
  {
    name: "list_submissions",
    description: "List student submissions for a coursework (status: TURNED_IN, RETURNED, NEW, late status, assigned grade).",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkId: { type: "string", description: "The coursework identifier (or '-' for all coursework in the course)." },
        userId: { type: "string", description: "Optional student filter ('me' for current user, or student user ID)." },
        states: {
          type: "array",
          items: { type: "string" },
          description: "Filter by submission states: NEW, CREATED, TURNED_IN, RETURNED, RECLAIMED_BY_STUDENT.",
        },
        pageSize: { type: "number", description: "Maximum number of submissions to return." },
      },
      required: ["courseId", "courseWorkId"],
    },
  },
  {
    name: "get_submission",
    description: "Get detailed student submission info including attached files, links, and assigned grade.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkId: { type: "string", description: "The coursework identifier." },
        submissionId: { type: "string", description: "The submission ID." },
      },
      required: ["courseId", "courseWorkId", "submissionId"],
    },
  },
  {
    name: "list_announcements",
    description: "List stream announcements, notices, and updates for a course.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        announcementStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter states: PUBLISHED, DRAFT, DELETED. Defaults to ['PUBLISHED'].",
        },
        pageSize: { type: "number", description: "Maximum number of announcements to return (default 20)." },
        orderBy: { type: "string", description: "Sort order, e.g. 'updateTime desc'." },
      },
      required: ["courseId"],
    },
  },
  {
    name: "list_coursework_materials",
    description: "List materials, syllabi, lecture slides, and resources posted under Classwork.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        courseWorkMaterialStates: {
          type: "array",
          items: { type: "string" },
          description: "Filter states: PUBLISHED, DRAFT, DELETED. Defaults to ['PUBLISHED'].",
        },
        pageSize: { type: "number", description: "Maximum number of materials to return (default 20)." },
      },
      required: ["courseId"],
    },
  },
  {
    name: "list_teachers",
    description: "List teachers of a course.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        pageSize: { type: "number", description: "Max teachers to return." },
      },
      required: ["courseId"],
    },
  },
  {
    name: "list_students",
    description: "List students enrolled in a course.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The unique identifier of the course." },
        pageSize: { type: "number", description: "Max students to return." },
      },
      required: ["courseId"],
    },
  },
  {
    name: "turn_in_assignment",
    description: "Turn in a student submission for grading.",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The course ID." },
        courseWorkId: { type: "string", description: "The coursework ID." },
        submissionId: { type: "string", description: "The submission ID." },
      },
      required: ["courseId", "courseWorkId", "submissionId"],
    },
  },
  {
    name: "reclaim_assignment",
    description: "Reclaim a turned-in student submission (unsubmit).",
    inputSchema: {
      type: "object",
      properties: {
        courseId: { type: "string", description: "The course ID." },
        courseWorkId: { type: "string", description: "The coursework ID." },
        submissionId: { type: "string", description: "The submission ID." },
      },
      required: ["courseId", "courseWorkId", "submissionId"],
    },
  },
];

const server = new Server(
  {
    name: "classroom-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args = {} } = request.params;

  try {
    if (name === "list_courses") {
      const params = new URLSearchParams();
      const states = args.courseStates || ["ACTIVE"];
      states.forEach((s) => params.append("courseStates", s));
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());
      if (args.studentId) params.set("studentId", args.studentId);
      if (args.teacherId) params.set("teacherId", args.teacherId);

      const res = await classroomFetch(`/courses?${params.toString()}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const courses = data.courses || [];

      let text = `Found ${courses.length} course(s):\n\n`;
      for (const c of courses) {
        text += `- **${c.name}**\n`;
        text += `  - ID: \`${c.id}\`\n`;
        if (c.section) text += `  - Section: ${c.section}\n`;
        if (c.room) text += `  - Room: ${c.room}\n`;
        text += `  - State: ${c.courseState}\n`;
        if (c.enrollmentCode) text += `  - Enrollment Code: \`${c.enrollmentCode}\`\n`;
        if (c.alternateLink) text += `  - Link: ${c.alternateLink}\n`;
        text += "\n";
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "get_course") {
      const res = await classroomFetch(`/courses/${args.courseId}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const c = await res.json();

      return {
        content: [{ type: "text", text: JSON.stringify(c, null, 2) }],
        isError: false,
      };
    }

    if (name === "list_coursework") {
      const params = new URLSearchParams();
      const states = args.courseWorkStates || ["PUBLISHED"];
      states.forEach((s) => params.append("courseWorkStates", s));
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());
      if (args.orderBy) params.set("orderBy", args.orderBy);

      const res = await classroomFetch(`/courses/${args.courseId}/courseWork?${params.toString()}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const list = data.courseWork || [];

      let text = `Found ${list.length} coursework item(s) in course \`${args.courseId}\`:\n\n`;
      for (const cw of list) {
        text += `### ${cw.title}\n`;
        text += `- **ID**: \`${cw.id}\`\n`;
        text += `- **Type**: ${cw.workType || "ASSIGNMENT"}\n`;
        text += `- **State**: ${cw.state}\n`;
        if (cw.maxPoints !== undefined) text += `- **Points**: ${cw.maxPoints}\n`;
        if (cw.dueDate) {
          const d = cw.dueDate;
          const t = cw.dueTime || {};
          text += `- **Due**: ${d.year}-${String(d.month).padStart(2, "0")}-${String(d.day).padStart(2, "0")}`;
          if (t.hours !== undefined) {
            text += ` ${String(t.hours).padStart(2, "0")}:${String(t.minutes || 0).padStart(2, "0")}`;
          }
          text += "\n";
        }
        if (cw.alternateLink) text += `- **Link**: ${cw.alternateLink}\n`;
        if (cw.description) text += `\n> ${cw.description.replace(/\n/g, "\n> ")}\n`;
        text += "\n---\n\n";
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "get_coursework") {
      const res = await classroomFetch(`/courses/${args.courseId}/courseWork/${args.courseWorkId}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const cw = await res.json();

      return {
        content: [{ type: "text", text: JSON.stringify(cw, null, 2) }],
        isError: false,
      };
    }

    if (name === "list_submissions") {
      const params = new URLSearchParams();
      if (args.userId) params.set("userId", args.userId);
      if (args.states) {
        args.states.forEach((s) => params.append("states", s));
      }
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());

      const res = await classroomFetch(
        `/courses/${args.courseId}/courseWork/${args.courseWorkId}/studentSubmissions?${params.toString()}`
      );
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const subs = data.studentSubmissions || [];

      let text = `Found ${subs.length} submission(s):\n\n`;
      for (const s of subs) {
        text += `- **Submission ID**: \`${s.id}\` (User ID: \`${s.userId}\`)\n`;
        text += `  - **State**: ${s.state}\n`;
        if (s.late !== undefined) text += `  - **Late**: ${s.late}\n`;
        if (s.assignedGrade !== undefined) text += `  - **Grade**: ${s.assignedGrade}\n`;
        if (s.draftGrade !== undefined) text += `  - **Draft Grade**: ${s.draftGrade}\n`;
        if (s.alternateLink) text += `  - **Link**: ${s.alternateLink}\n`;
        text += "\n";
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "get_submission") {
      const res = await classroomFetch(
        `/courses/${args.courseId}/courseWork/${args.courseWorkId}/studentSubmissions/${args.submissionId}`
      );
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const sub = await res.json();

      return {
        content: [{ type: "text", text: JSON.stringify(sub, null, 2) }],
        isError: false,
      };
    }

    if (name === "list_announcements") {
      const params = new URLSearchParams();
      const states = args.announcementStates || ["PUBLISHED"];
      states.forEach((s) => params.append("announcementStates", s));
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());
      if (args.orderBy) params.set("orderBy", args.orderBy);

      const res = await classroomFetch(`/courses/${args.courseId}/announcements?${params.toString()}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const list = data.announcements || [];

      let text = `Found ${list.length} announcement(s):\n\n`;
      for (const a of list) {
        text += `### Announcement (${a.updateTime || a.creationTime})\n`;
        text += `- **ID**: \`${a.id}\`\n`;
        if (a.alternateLink) text += `- **Link**: ${a.alternateLink}\n`;
        if (a.text) text += `\n${a.text}\n`;
        text += "\n---\n\n";
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "list_coursework_materials") {
      const params = new URLSearchParams();
      const states = args.courseWorkMaterialStates || ["PUBLISHED"];
      states.forEach((s) => params.append("courseWorkMaterialStates", s));
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());

      const res = await classroomFetch(`/courses/${args.courseId}/courseWorkMaterials?${params.toString()}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const list = data.courseWorkMaterial || [];

      let text = `Found ${list.length} material item(s):\n\n`;
      for (const m of list) {
        text += `### ${m.title}\n`;
        text += `- **ID**: \`${m.id}\`\n`;
        if (m.alternateLink) text += `- **Link**: ${m.alternateLink}\n`;
        if (m.description) text += `\n${m.description}\n`;
        text += "\n---\n\n";
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "list_teachers") {
      const params = new URLSearchParams();
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());

      const res = await classroomFetch(`/courses/${args.courseId}/teachers?${params.toString()}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const teachers = data.teachers || [];

      let text = `Found ${teachers.length} teacher(s):\n\n`;
      for (const t of teachers) {
        const p = t.profile || {};
        const name = p.name ? p.name.fullName : "Unknown";
        text += `- **${name}** (User ID: \`${t.userId}\`)\n`;
        if (p.emailAddress) text += `  - Email: ${p.emailAddress}\n`;
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "list_students") {
      const params = new URLSearchParams();
      if (args.pageSize) params.set("pageSize", args.pageSize.toString());

      const res = await classroomFetch(`/courses/${args.courseId}/students?${params.toString()}`);
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      const data = await res.json();
      const students = data.students || [];

      let text = `Found ${students.length} student(s):\n\n`;
      for (const s of students) {
        const p = s.profile || {};
        const name = p.name ? p.name.fullName : "Unknown";
        text += `- **${name}** (User ID: \`${s.userId}\`)\n`;
        if (p.emailAddress) text += `  - Email: ${p.emailAddress}\n`;
      }

      return {
        content: [{ type: "text", text: text.trim() }],
        isError: false,
      };
    }

    if (name === "turn_in_assignment") {
      const res = await classroomFetch(
        `/courses/${args.courseId}/courseWork/${args.courseWorkId}/studentSubmissions/${args.submissionId}:turnIn`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({}),
        }
      );
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      return {
        content: [{ type: "text", text: `Successfully turned in submission ${args.submissionId}.` }],
        isError: false,
      };
    }

    if (name === "reclaim_assignment") {
      const res = await classroomFetch(
        `/courses/${args.courseId}/courseWork/${args.courseWorkId}/studentSubmissions/${args.submissionId}:reclaim`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({}),
        }
      );
      if (!res.ok) throw new Error(`Google Classroom API error: ${await res.text()}`);
      return {
        content: [{ type: "text", text: `Successfully reclaimed (unsubmitted) submission ${args.submissionId}.` }],
        isError: false,
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (err) {
    return {
      content: [{ type: "text", text: `Error executing ${name}: ${err.message}` }],
      isError: true,
    };
  }
});

async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

run().catch((err) => {
  console.error("Fatal error running server:", err);
  process.exit(1);
});
