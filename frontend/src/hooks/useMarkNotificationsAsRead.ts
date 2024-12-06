import { useState } from "react";
import { markNotificationsAsRead } from "../api/notifications";

const useMarkNotificationsAsRead = () => {
    const [marking, setMarking] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const markAsRead = async (notificationIds: number[]) => {
        try {
            setMarking(true);
            await markNotificationsAsRead(notificationIds);
            return true;
        } catch (err) {
            setError("Failed to mark notifications as read.");
            return false;
        } finally {
            setMarking(false);
        }
    };

    return {
        markAsRead,
        marking,
        error,
    };
};

export default useMarkNotificationsAsRead;
