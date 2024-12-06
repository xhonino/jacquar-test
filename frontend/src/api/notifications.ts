import axios from "axios";
import { NotificationListResponse } from '../types/notifications';

const API_ENDPOINT = process.env.REACT_APP_API_ENDPOINT;

// Fetch notifications with limit and offset
export const fetchNotifications = async (
    userId: string,
    skip: number,
    limit: number
): Promise<NotificationListResponse> => {
    const response = await axios.get(`${API_ENDPOINT}/notifications`, {
        params: { user_id: userId, skip, limit },
    });
    return response.data;
};

// Mark notifications as read
export const markNotificationsAsRead = async (
    notificationIds: number[]
): Promise<void> => {
    await axios.post(`${API_ENDPOINT}/notifications/read`, notificationIds);
};
