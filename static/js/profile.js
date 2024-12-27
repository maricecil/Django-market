// 즉시 실행 함수로 래핑하여 이벤트 중복 방지
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('profileEditForm');
        if (!form) return;
        
        // 이벤트 리스너가 이미 등록되었는지 확인
        if (form.dataset.initialized) return;
        form.dataset.initialized = 'true';

        form.addEventListener('submit', async function(e) {
            e.preventDefault();  // 폼 기본 제출 동작 방지
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
                
                const data = await response.json();
                console.log('서버 응답:', data);  // 응답 데이터 확인
                
                if (data.status === 'success') {
                    // 프로필 정보 업데이트
                    updateFormValues(data.profile_data);
                    alert('프로필이 성공적으로 업데이트되었습니다.');
                    
                    // 페이지 새로고침 방지
                    return false;
                } else {
                    alert(data.message || '프로필 업데이트 중 오류가 발생했습니다.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('프로필 업데이트 중 오류가 발생했습니다.');
            }
        });
    });
})();

function updateFormValues(data) {
    if (!data) return;
    
    try {
        // 바이오 업데이트
        const bioElement = document.querySelector('.text-gray-500.mt-1');
        if (bioElement) bioElement.textContent = data.bio || '안녕하세요!';

        // 학교 정보 컨테이너
        const schoolContainer = document.querySelector('.inline-flex.items-center.gap-2.px-4.py-2.bg-white\\/80');
        if (schoolContainer) {
            // 기존 내용을 모두 비우고 새로 구성
            schoolContainer.innerHTML = '';
            
            // 지역 정보가 있는 경우
            if (data.location) {
                const locationSpan = document.createElement('span');
                locationSpan.className = 'font-medium';
                locationSpan.textContent = data.location;
                schoolContainer.appendChild(locationSpan);
                
                // 다음 정보가 있는 경우에만 구분점 추가
                if (data.school || data.grade || data.department) {
                    const dot = document.createElement('span');
                    dot.className = 'w-1 h-1 bg-gray-300 rounded-full';
                    schoolContainer.appendChild(dot);
                }
            }
            
            // 학교 정보 추가
            if (data.school) {
                const schoolSpan = document.createElement('span');
                schoolSpan.className = 'font-medium';
                schoolSpan.textContent = data.school;
                schoolContainer.appendChild(schoolSpan);
            }

            // 학년 정보 추가
            if (data.grade) {
                const dot = document.createElement('span');
                dot.className = 'w-1 h-1 bg-gray-300 rounded-full';
                schoolContainer.appendChild(dot);

                const gradeSpan = document.createElement('span');
                gradeSpan.textContent = `${data.grade}학년`;
                schoolContainer.appendChild(gradeSpan);
            }

            // 학과 정보 추가
            if (data.department) {
                const dot = document.createElement('span');
                dot.className = 'w-1 h-1 bg-gray-300 rounded-full';
                schoolContainer.appendChild(dot);

                const deptSpan = document.createElement('span');
                deptSpan.textContent = data.department;
                schoolContainer.appendChild(deptSpan);
            }
        }

        // 개인 정보 업데이트 부분만 수정
        const personalInfoContainer = document.querySelector('.mt-3.flex.items-center.gap-3.text-sm.text-gray-600');
        if (personalInfoContainer) {
            const flexContainer = personalInfoContainer.querySelector('.flex.items-center.gap-2');
            if (!flexContainer) return;

            // 기존 사이즈 정보 찾기
            const existingSizeSpan = Array.from(flexContainer.querySelectorAll('span')).find(span => 
                !span.textContent.includes('cm') && 
                !span.textContent.includes('kg') && 
                !['남성', '여성'].includes(span.textContent.trim())
            );

            // 사이즈 정보 업데이트 또는 추가
            if (data.usual_size) {
                if (existingSizeSpan) {
                    existingSizeSpan.textContent = data.usual_size;
                } else {
                    const sizeSpan = document.createElement('span');
                    sizeSpan.className = 'px-3 py-1 bg-white/80 backdrop-blur-sm rounded-lg shadow-sm';
                    sizeSpan.textContent = data.usual_size;
                    flexContainer.appendChild(sizeSpan);
                }
            } else if (existingSizeSpan) {
                // 사이즈 정보가 없는 경우 기존 span 제거
                existingSizeSpan.remove();
            }

            // 나머지 정보 업데이트 (성별, 키, 몸무게)
            const spans = flexContainer.querySelectorAll('span');
            spans.forEach(span => {
                const text = span.textContent.trim();
                if ((text === '여성' || text === '남성') && data.gender) {
                    span.textContent = data.gender === 'F' ? '여성' : '남성';
                } else if (text.includes('cm') && data.height) {
                    span.textContent = `${data.height}cm`;
                } else if (text.includes('kg') && data.weight) {
                    span.textContent = `${data.weight}kg`;
                }
            });
        }

        // 성별 라디오 버튼 업데이트 부분만 수정
        const genderContainer = document.querySelector('.flex.gap-4');
        if (genderContainer) {
            const maleLabel = genderContainer.querySelector('label:first-child');
            const femaleLabel = genderContainer.querySelector('label:last-child');
            const maleInput = maleLabel.querySelector('input[value="M"]');
            const femaleInput = femaleLabel.querySelector('input[value="F"]');

            console.log('성별 데이터:', data.gender); // 디버깅용
            console.log('남성 라벨:', maleLabel); // 디버깅용
            console.log('여성 라벨:', femaleLabel); // 디버깅용

            if (data.gender === 'M') {
                maleLabel.classList.add('bg-black', 'text-white');
                maleLabel.classList.remove('hover:bg-gray-50');
                femaleLabel.classList.remove('bg-black', 'text-white');
                maleInput.checked = true;
                femaleInput.checked = false;
            } else if (data.gender === 'F') {
                femaleLabel.classList.add('bg-black', 'text-white');
                femaleLabel.classList.remove('hover:bg-gray-50');
                maleLabel.classList.remove('bg-black', 'text-white');
                femaleInput.checked = true;
                maleInput.checked = false;
            }
        }

        console.log('프로필 업데이트 완료:', data);

    } catch (error) {
        console.error('프로필 업데이트 중 오류:', error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 

async function toggleFollow(userId) {
    try {
        const response = await fetch(`/accounts/${userId}/follow/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // 모든 팔로우 버튼 업데이트
            const buttons = document.querySelectorAll(`[data-user-id="${userId}"]`);
            buttons.forEach(button => {
                updateFollowButton(button, data.is_following);
                button.dataset.following = data.is_following;
            });
            
            // 팔재 사용자의 팔로잉 수만 업데이트
            const followingCountElements = document.querySelectorAll('button[onclick*="showFollowModal(\'following\')"] span.font-bold');
            followingCountElements.forEach(element => {
                const currentCount = parseInt(element.textContent || 0);
                element.textContent = data.is_following ? currentCount + 1 : currentCount - 1;
            });
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 버튼 상태 업데이트 함수 추가
function updateFollowButton(button, isFollowing) {
    // 이벤트 리스너 제거
    button.removeEventListener('mouseenter', button._handleMouseEnter);
    button.removeEventListener('mouseleave', button._handleMouseLeave);

    if (isFollowing) {
        button.classList.remove('bg-orange-500', 'text-white');
        button.classList.add('bg-gray-200', 'text-gray-800');
        button.textContent = '팔로잉';
        
        // 호버 이벤트 핸들러
        button._handleMouseEnter = () => {
            button.textContent = '팔로우 취소';
            button.classList.add('bg-red-100', 'text-red-600');
            button.classList.remove('bg-gray-200', 'text-gray-800');
        };
        
        button._handleMouseLeave = () => {
            button.textContent = '팔로잉';
            button.classList.remove('bg-red-100', 'text-red-600');
            button.classList.add('bg-gray-200', 'text-gray-800');
        };
        
        // 새 이벤트 리스너 추가
        button.addEventListener('mouseenter', button._handleMouseEnter);
        button.addEventListener('mouseleave', button._handleMouseLeave);
    } else {
        button.classList.remove('bg-gray-200', 'text-gray-800', 'bg-red-100', 'text-red-600');
        button.classList.add('bg-orange-500', 'text-white');
        button.textContent = '팔로우';
        
        // 팔로우 취소 상태에서는 호버 이벤트 제거
        button._handleMouseEnter = null;
        button._handleMouseLeave = null;
    }
    
    // 버튼의 상태 데이터 업데이트
    button.dataset.following = isFollowing.toString();
} 

async function showFollowModal(type) {
    const modal = document.getElementById('followModal');
    const modalTitle = document.getElementById('modalTitle');
    const followList = document.getElementById('followList');
    
    modalTitle.textContent = type === 'followers' ? '팔로워 목록' : '팔로잉 목록';
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    
    try {
        const sellerId = document.querySelector('[data-seller-id]').dataset.sellerId;
        const response = await fetch(`/accounts/follow-list/${type}/${sellerId}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'error') {
            throw new Error(data.message);
        }
        
        if (!data.users || data.users.length === 0) {
            followList.innerHTML = `
                <div class="text-center py-8 text-gray-500">
                    ${type === 'followers' ? '아직 팔로워가 없습니다.' : '아직 팔로잉하는 사용자가 없습니다.'}
                </div>
            `;
            return;
        }
        
        followList.innerHTML = data.users.map(user => `
            <div class="flex items-center justify-between py-3 hover:bg-gray-50 px-3 rounded-lg">
                <a href="/accounts/profile/${user.id}/" class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full overflow-hidden bg-gray-100">
                        ${user.profile_image ? 
                            `<img src="${user.profile_image}" alt="" class="w-full h-full object-cover">` :
                            `<div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-yellow-200 to-yellow-400">
                                <span class="text-lg font-bold text-white">${user.username[0].toUpperCase()}</span>
                            </div>`
                        }
                    </div>
                    <div>
                        <span class="font-medium">${user.username}</span>
                        ${user.bio ? `<p class="text-sm text-gray-500">${user.bio}</p>` : ''}
                    </div>
                </a>
                ${user.can_follow ? `
                    <button 
                        onclick="handleFollowClick(event, '${user.id}')"
                        data-user-id="${user.id}"
                        data-following="${user.is_following}"
                        class="follow-button px-4 py-1.5 rounded-full text-sm font-medium ${
                            user.is_following ? 
                            'bg-gray-200 text-gray-800' : 
                            'bg-orange-500 text-white'
                        } transition-colors">
                        ${user.is_following ? '팔로잉' : '팔로우'}
                    </button>
                ` : ''}
            </div>
        `).join('');

        // 모달이 열린 후 버튼들에 이벤트 리스너 추가
        const buttons = followList.querySelectorAll('.follow-button');
        buttons.forEach(button => {
            const isFollowing = button.dataset.following === 'true';
            updateFollowButton(button, isFollowing);
        });
        
    } catch (error) {
        console.error('Error:', error);
        followList.innerHTML = `<p class="text-center text-gray-500 py-4">목록을 불러오는데 실패했습니다: ${error.message}</p>`;
    }
} 

// 전역 함수로 추가
window.handleFollowClick = async function(event, userId) {
    event.preventDefault();
    event.stopPropagation();
    await toggleFollow(userId);
} 
