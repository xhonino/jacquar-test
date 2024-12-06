import React from 'react';
import Avatar from './Avatar';
import { Notification as NotificationType } from '../types/notifications';

type NotificationProps = Omit<NotificationType, 'notification_date' | 'actor_id' | 'post_id' | 'id'>;

const Notification: React.FC<NotificationProps> = ({
  actor_name: actorName,
  previous_actor_name: previousActorName,
  actors_count: actorsCount,
  actor_avatar: actorAvatar,
  comment,
  type: notificationType,
  is_read: isRead,
  post_title: postTitle,
}) => {
  const getNotificationText = () => {
    if (notificationType === 'LIKE') {
      const fullText = actorName + (previousActorName ? `, ${previousActorName}` : '') + (actorsCount > 2 ? ` and ${actorsCount - 2} others` : '') + ' liked your post: ';
      const truncatedPostTitle = postTitle.length > 125 - fullText.length ? postTitle.substring(0, 125 - fullText.length - 3) + '...' : postTitle;
      return (
        <span>
          <span className="text-blue-600 font-semibold">
            {actorName}
            {previousActorName ? `, ${previousActorName}` : ''}
            {actorsCount > 2 ? ` and ${actorsCount - 2} others` : ''}
          </span>
          {' liked'}
          <span className="font-semibold">
            {' your post: '}
          </span>
          "{truncatedPostTitle}"
        </span>
      );
    }
    if (notificationType === 'COMMENT') {
      const fullText = actorName + (previousActorName ? `, ${previousActorName}` : '') + (actorsCount > 2 ? ` and ${actorsCount - 2} others` : '') + ' commented on your post: ';
      const truncatedComment = String(comment).length > 125 - fullText.length ? String(comment).substring(0, 125 - fullText.length - 3) + '...' : comment;
      return (
        <span>
          <span className="text-blue-600 font-semibold">
            {actorName}
            {previousActorName ? `, ${previousActorName}` : ''}
            {actorsCount > 2 ? ` and ${actorsCount - 2} others` : ''}
          </span>
          {' commented on'}
          <span className="font-semibold">
            {' your post: '}
          </span>
          {truncatedComment ? `"${truncatedComment}"` : `"${truncatedComment}"`}
        </span>
      );
    }
    return '';
  };


  return (
    <div
      className={`flex items-start ${isRead ? 'bg-white' : 'bg-gray-100'} border-b`}
    >
      <Avatar actorAvatar={actorAvatar} />
      <div className="flex-1 my-auto py-2 pr-2" >
        <p className="text-sm text-gray-700" >
          {getNotificationText()}
        </p>
      </div>
    </div>
  );
};

export default Notification;
