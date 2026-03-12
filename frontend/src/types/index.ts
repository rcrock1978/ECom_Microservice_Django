export type ApiError = {
  error: {
    code: string;
    message: string;
    details?: Array<{ field?: string; message: string }>;
  };
};

export type ApiSuccess<T> = {
  data: T;
  meta?: {
    page?: number;
    page_size?: number;
    total?: number;
  };
};
