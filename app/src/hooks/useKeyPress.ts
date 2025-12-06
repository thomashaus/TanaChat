import { useEffect } from 'react';

export function useKeyPress(targetKey: string, callback: () => void, metaKey: boolean = false) {
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            const isMetaPressed = metaKey ? (event.metaKey || event.ctrlKey) : true;

            if (isMetaPressed && event.key.toLowerCase() === targetKey.toLowerCase()) {
                event.preventDefault();
                callback();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [targetKey, callback, metaKey]);
}
