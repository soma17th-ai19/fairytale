export type User = {
  id: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  expires_in: number;
  user: User;
};

export type AuthPayload = {
  email: string;
  password: string;
};

export type ChildCreatePayload = {
  name: string;
  age: number;
  personality: string;
  favorite_character: string;
};

export type MessageResponse = {
  message: string;
};

export type StoryGeneratePayload = {
  child_id: string;
  situation: string;
  lesson: string;
  mood: string;
  category: string;
};

type ApiErrorBody = {
  detail?: string | Array<{ msg?: string }>;
};

const API_BASE_URL = "/api/v1";

async function parseApiError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as ApiErrorBody;

    if (typeof body.detail === "string") {
      return body.detail;
    }

    if (Array.isArray(body.detail)) {
      return body.detail
        .map((item) => item.msg)
        .filter(Boolean)
        .join(", ");
    }
  } catch {
    // Fall through to the generic status message.
  }

  return `Request failed with ${response.status}`;
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers
    },
    ...options
  });

  if (!response.ok) {
    throw new Error(await parseApiError(response));
  }

  return response.json() as Promise<T>;
}

export function register(payload: AuthPayload): Promise<AuthResponse> {
  return request<AuthResponse>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function login(payload: AuthPayload): Promise<AuthResponse> {
  return request<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function getCurrentUser(token: string): Promise<User> {
  return request<User>("/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
}

export function createChild(
  payload: ChildCreatePayload,
  token: string
): Promise<MessageResponse> {
  return request<MessageResponse>("/children", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });
}

export function generateStory(
  payload: StoryGeneratePayload
): Promise<MessageResponse> {
  return request<MessageResponse>("/stories/generate", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
