import React from 'react';

interface AvatarProps {
  actorAvatar?: string;
}

const Avatar: React.FC<AvatarProps> = ({ actorAvatar }) => {
  return (
    <div>
      {actorAvatar ? (
        <img className='w-12 h-12 rounded-[1px] m-2' src={`/portraits/${actorAvatar}`} alt='Actor Avatar' />
      ) : (
        <div className='w-12 h-12 rounded-[1px] m-2 bg-gray-400'>
        </div>
      )}
    </div>
  );
};

export default Avatar;
