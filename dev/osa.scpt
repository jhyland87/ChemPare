tell application "Brave Browser"
    open location "http://google.com"
    -- if not (exists window 2) then reopen
    -- set URL of active tab of window 2 to "http://google.com"
    -- activate
    -- tell window 1 to tell active tab
    --     delay 0.5
    --     open location "http://google.com"
    -- end tell
end tell


-- tell application "Brave Browser"
--     activate
-- 	tell application "System Events" to tell process "Brave Browser"
-- 		set position of window 1 to { 0, 50 }
-- 		set size of window 1 to { 1350, 950 }
-- 		set value of attribute "AXFullScreen" of window 1 to true
--         set URL of active tab of window 2 to "http://google.com"
-- 	end tell
-- end tell
