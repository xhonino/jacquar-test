import React, { useState } from 'react';
import { FaGlobeAmericas } from "react-icons/fa";
import useNotifications from "../hooks/useNotifications";
import useMarkNotificationsAsRead from "../hooks/useMarkNotificationsAsRead";
import Notification from './Notification';
import { Notification as NotificationType } from '../types/notifications';

interface OutputNotificationListProps {
    userId?: string;
}

const OutputNotificationList: React.FC<OutputNotificationListProps> = ({ userId = "1" }) => {
    const [visibleCount, setVisibleCount] = useState<number>(5);
    const [isListVisible, setIsListVisible] = useState<boolean>(false);

    const {
        notifications,
        loading,
        error,
        loadMore,
        hasMore,
    } = useNotifications(userId);


    const { markAsRead } = useMarkNotificationsAsRead();
    const markAsReadLocal = async (notifications: NotificationType[]) => {
        const notificationIds = notifications.map((notification) => notification.id);
        await markAsRead(notificationIds);
        notifications.forEach((notification) => {
            notification.is_read = true;
        });
    }


    const unreadNotifications = notifications.filter((notification) => !notification.is_read);

    // Toggles the visibility of the notification list
    const toggleNotificationList = async () => {
        setIsListVisible((prev) => !prev);
        await markAsReadLocal(unreadNotifications);
    };

    // Load more notifications logic
    const handleLoadMore = async () => {
        loadMore();
        setVisibleCount((prev) => prev + 5);
        await markAsReadLocal(unreadNotifications)
    };

    return (
        <div className="relative">
            {/* Pass toggleNotificationList directly to GlobeIcon */}
            <GlobeIcon onClick={toggleNotificationList} notificationCount={unreadNotifications.length} />
            {isListVisible && (
                <div className="w-[500px] mx-auto border shadow-md absolute top-10 right-0 bg-white max-h-[600px] overflow-y-auto scrollbar-hide">
                    {loading && <p className="text-center py-2">Loading...</p>}
                    {error && <p className="text-center py-2 text-red-600">{error}</p>}
                    {notifications.length === 0 ? (
                        <p className="text-center py-2 text-gray-400">No new notifications</p>
                    ) : (
                        <>
                            {notifications.slice(0, visibleCount).map((notification: NotificationType) => (
                                <Notification key={notification.id} {...notification} />
                            ))}
                            <button
                                onClick={handleLoadMore}
                                className={`w-full py-2 text-center ${hasMore ? 'text-blue-600 hover:bg-gray-100' : 'text-gray-400 cursor-not-allowed'}`}
                                disabled={!hasMore}
                            >
                                Load More
                            </button>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

interface GlobeIconProps {
    onClick: () => void;
    notificationCount?: number;
}

// GlobeIcon component handles the onClick to toggle visibility
const GlobeIcon: React.FC<GlobeIconProps> = ({ onClick, notificationCount }) => {
    return (
        <div className="relative">
            {/* Toggle notification list on button click */}
            <button className="w-10 h-10 rounded-full flex items-center justify-center">
                <FaGlobeAmericas size={24} color='white' onClick={onClick} />
                {notificationCount && notificationCount > 0 ? (
                    <span className="absolute top-0 right-0 bg-red-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {notificationCount}
                    </span>
                ) : null}
            </button>
        </div>
    );
};


export default OutputNotificationList;