export interface Notification {
    id: number;
    actor_id: string;
    actor_name: string;
    actor_avatar: string;
    notification_date: string; // ISO format
    previous_actor_name?: string | null;
    type: "LIKE" | "COMMENT";
    actors_count: number;
    comment?: string | null;
    post_id: string;
    post_title: string;
    is_read: Boolean;
}

export interface NotificationListResponse {
    feed: Notification[] | null;
}

export interface MarkNotificationsRequest {
    notificationIds: number[];
}
