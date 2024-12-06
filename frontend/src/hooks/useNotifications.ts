import { useState, useEffect } from "react";
import { fetchNotifications } from "../api/notifications";
import { Notification } from "../types/notifications";

const useNotifications = (userId: string) => {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [offset, setOffset] = useState<number>(0);
    const [hasMore, setHasMore] = useState<boolean>(true);

    const limit = 5; // Number of notifications to fetch per request

    const fetchMoreNotifications = async () => {
        try {
            setLoading(true);
            const response = await fetchNotifications(userId, offset, limit);
            const data = response.feed || [];
            if (data.length < limit) {
                setHasMore(false);
            }
            setNotifications((prev) => [...prev, ...data]);
        } catch (err) {
            setError("Failed to fetch notifications.");
        } finally {
            setLoading(false);
        }
    };

    const loadMore = () => {
        setOffset((prev) => prev + limit);
    };

    useEffect(() => {
        fetchMoreNotifications();
    }, [offset]);
    
    return {
        notifications,
        loading,
        error,
        loadMore,
        hasMore,
    };
};

export default useNotifications;
